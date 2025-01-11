import pytest
import os

import advent.utils.int_math as util

def test_lcm():
    assert util.lcm(1, 5) == 5
    assert util.lcm(5, 7) == 35
    assert util.lcm(4, 6) == 12

def test_inverse_mod_n():
    x = util.inverse_modn(5, 7)
    assert (5*x) % 7 == 1
    with pytest.raises(ValueError):
        util.inverse_modn(5, 10)

def test_ext_gcd():
    d, s, t = util.extgcd(1, 5)
    assert d == 1
    assert s*1 + t*5 == 1

    d, s, t = util.extgcd(5, 10)
    assert d == 5
    assert s*5 + t*10 == 5

    d, s, t = util.extgcd(3, 9)
    assert d == 3
    assert s*3 + t*9 == 3

    d, s, t = util.extgcd(15, 35)
    assert d == 5
    assert s*15 + t*35 == 5

def test_solve_int_lin_comb():
    x, y = util.solve_int_lin_comb(1, 5, 2)
    assert 1*x + 5*y == 2
    with pytest.raises(ValueError):
        util.solve_int_lin_comb(3, 9, 4)
    x, y = util.solve_int_lin_comb(101, 103, 1)
    assert 101*x + 103*y == 1

def brute_int_lin_comb_min_solve(p, q, n):
    x = 0
    while True:
        # p*x + q*y == n
        if (n - p*x) % q == 0:
            return x, (n - p*x) // q
        x += 1

def test_int_lin_comb_min_solve():
    for p,q,n in [(1,5,2), (3,9,15), (101, 103, 1), (101, 103, 23)]:
        x, y = util.int_lin_comb_min_solve(p, q, n)
        assert p*x + q*y == n
        xx, yy = brute_int_lin_comb_min_solve(p, q, n)
        assert x == xx and y == yy
    