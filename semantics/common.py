#!/usr/bin/env python
# vim: set fileencoding=UTF-8 :


import gmpy2
from gmpy2 import mpq, mpfr


def ulp(v):
    return mpq(2) ** v.as_mantissa_exp()[1]


def round_op(f):
    def wrapped(v1, v2, mode):
        with gmpy2.local_context(round=mode):
            return f(v1, v2)
    return wrapped


if __name__ == '__main__':
    gmpy2.set_context(gmpy2.ieee(32))
    print float(ulp(mpfr('0.1')))
    mult = lambda x, y: x * y
    args = [mpfr('0.3'), mpfr('2.6')]
    print round_op(mult)(*(args + [gmpy2.RoundDown]))
    print round_op(mult)(*(args + [gmpy2.RoundUp]))
