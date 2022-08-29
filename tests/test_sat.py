#! /usr/bin/env python3.8


import pytest

from normal_form.cnf import Bool, cnf
from normal_form.sat import (cnf_bruteforce_satcheck, cnf_minisat_satcheck,
                             cnf_pysat_satcheck, generate_assignments)


def test_generate_assignments() -> None:
    assert {1: Bool.TRUE} in list(generate_assignments(cnf([[1]])))
    assert {1: Bool.FALSE} in list(generate_assignments(cnf([[1]])))
    assert {1: Bool.TRUE} in list(generate_assignments(cnf([[-1]])))
    assert {1: Bool.FALSE} in list(generate_assignments(cnf([[-1]])))
    assert list(generate_assignments(cnf([[Bool.TRUE]]))) == [{}]
    assert list(generate_assignments(cnf([[Bool.FALSE]]))) == [{}]
    assert {1: Bool.TRUE, 2: Bool.TRUE} in list(generate_assignments(cnf([[1, -2]])))
    assert {1: Bool.TRUE, 2: Bool.FALSE} in list(generate_assignments(cnf([[1, -2]])))
    assert {1: Bool.FALSE, 2: Bool.TRUE} in list(generate_assignments(cnf([[1, -2]])))
    assert {1: Bool.FALSE, 2: Bool.FALSE} in list(generate_assignments(cnf([[1, -2]])))
    assert list(generate_assignments(cnf([[1, -1]]))) == [{}]
    assert list(generate_assignments(cnf([[1, -1]]))) == [{}]
    with pytest.raises(ValueError):
        list(generate_assignments(cnf([[]])))


def test_cnf_bruteforce_satcheck() -> None:
    satchecker = cnf_bruteforce_satcheck
    assert satchecker(cnf([[Bool.TRUE]]))
    assert not satchecker(cnf([[Bool.FALSE]]))
    assert satchecker(cnf([[1]]))
    assert satchecker(cnf([[-1]]))
    assert satchecker(cnf([[1], [Bool.TRUE]]))
    assert not satchecker(cnf([[1], [Bool.FALSE]]))
    assert satchecker(cnf([[1, Bool.FALSE]]))
    assert not satchecker(cnf([[1], [-1]]))
    assert not satchecker(cnf([[1, 2], [1, -2], [-1, 2], [-1, -2]]))
    assert not satchecker(cnf([[1, 2], [-1, 2], [-2, 3], [-2, -3]]))
    assert not satchecker(cnf([[1, 2], [1, -2], [-1, 2], [-1, 3], [-2, -3]]))


def test_cnf_pysat_satcheck() -> None:
    satchecker = cnf_pysat_satcheck
    assert satchecker(cnf([[Bool.TRUE]]))
    assert not satchecker(cnf([[Bool.FALSE]]))
    assert satchecker(cnf([[1]]))
    assert satchecker(cnf([[-1]]))
    assert satchecker(cnf([[1], [Bool.TRUE]]))
    assert not satchecker(cnf([[1], [Bool.FALSE]]))
    assert satchecker(cnf([[1, Bool.FALSE]]))
    assert not satchecker(cnf([[1], [-1]]))
    assert not satchecker(cnf([[1, 2], [1, -2], [-1, 2], [-1, -2]]))
    assert not satchecker(cnf([[1, 2], [-1, 2], [-2, 3], [-2, -3]]))
    assert not satchecker(cnf([[1, 2], [1, -2], [-1, 2], [-1, 3], [-2, -3]]))


def test_cnf_minisat_satcheck() -> None:
    satchecker = cnf_minisat_satcheck
    assert satchecker(cnf([[Bool.TRUE]]))
    assert not satchecker(cnf([[Bool.FALSE]]))
    assert satchecker(cnf([[1]]))
    assert satchecker(cnf([[-1]]))
    assert satchecker(cnf([[1], [Bool.TRUE]]))
    assert not satchecker(cnf([[1], [Bool.FALSE]]))
    assert satchecker(cnf([[1, Bool.FALSE]]))
    assert not satchecker(cnf([[1], [-1]]))
    assert not satchecker(cnf([[1, 2], [1, -2], [-1, 2], [-1, -2]]))
    assert not satchecker(cnf([[1, 2], [-1, 2], [-2, 3], [-2, -3]]))
    assert not satchecker(cnf([[1, 2], [1, -2], [-1, 2], [-1, 3], [-2, -3]]))
