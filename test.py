import gmpy2
import ce.logger as logger
from ce.common import timeit
from ce.expr import Expr
from ce.analysis import analyse, Plot, expr_frontier
import ce.transformer.utils as utils


gmpy2.set_context(gmpy2.ieee(32))
logger.set_context(level=logger.levels.info)
Expr.__repr__ = Expr.__str__

DEPTH = 2


@timeit
def closure(e, v):
    c = utils.closure(e)
    return c, set(expr_frontier(c, v))


@timeit
def depth(e, v):
    c = utils.closure(e, depth=DEPTH)
    return c, set(expr_frontier(c, v))


@timeit
def greedy(e, v):
    return None, utils.greedy_frontier_closure(e, depth=None, var_env=v)


@timeit
def frontier_trace(e, v):
    c = utils.frontier_trace(e, var_env=v, depth=DEPTH)
    return c, set(expr_frontier(c, v))


@timeit
def greedy_trace(e, v):
    c = utils.greedy_trace(e, v, depth=3)
    return c, set(expr_frontier(c, v))


@timeit
def multi_width_greedy_trace(e, v):
    c = utils.multi_width_greedy_trace(e, v)
    return c, set(expr_frontier(c, v))


def analyse_and_plot(e, v, analyser=None):
    logger.set_context(level=logger.levels.info)
    Expr.__repr__ = Expr.__str__
    logger.info(Expr(e).error(v, gmpy2.ieee(32).precision))
    p = Plot(log=(analyser is not None))
    for f in [greedy_trace, frontier_trace]:
        derived, front = f(e, v)
        derived = derived or front
        logger.info(f.__name__, len(front), len(derived))
        p.add(analyse(derived, v, analyser), legend=f.__name__,
              alpha=0.7, linestyle='-', linewidth=1, marker='.')
    p.add(analyse(e, v), frontier=False, legend='original', marker='.')
    p.save('a.pdf')
    p.show()


e = """
    (a + a + b) * (a + b + b) * (b + b + c) *
    (b + c + c) * (c + c + a) * (c + a + a) |
    (1 + b + c) * (a + 1 + b) * (a + b + 1)
    """
v = {
    'a': ['1', '2'],
    'b': ['10', '20'],
    'c': ['100', '200'],
}
a = 'vary_width'
analyse_and_plot(e, v, a)
