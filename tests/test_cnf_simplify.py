#!/usr/bin/env python3.8
"""Tests for cnf_simplify.py."""

from hypothesis import given
from hypothesis import strategies as st

from normal_form.cnf import Clause, Cnf, clause, cnf, lit
from normal_form.cnf_simplify import (differing_lits,
                                      equivalent_smaller_clause, reduce_cnf,
                                      subclause_reduction)
from normal_form.sat import cnf_pysat_satcheck


def test_differing_lits() -> None:
    c1: Clause = clause([1, 2, -3])
    c2: Clause = clause([-1, -2, -3])
    assert not differing_lits(c1, c1)
    assert not differing_lits(c2, c2)
    assert differing_lits(c1, c2) == {lit(1), lit(2), lit(-1), lit(-2)}
    assert differing_lits(c1, c2) == differing_lits(c2, c1)


def test_equivalent_smaller_clause() -> None:
    c1: Clause = clause([1, 2, -3])
    c2: Clause = clause([1, 2, 3])
    assert equivalent_smaller_clause(c1, c2) == clause([1, 2])


def test_reduce_cnf() -> None:
    x: Cnf = cnf([[1, 2, -3], [1, 2, 3], [-1, -2, 3], [4, 5]])
    x_red: Cnf = cnf([[1, 2], [-1, -2, 3], [4, 5]])
    assert reduce_cnf(x) == x_red


def test_subclause_reduction() -> None:
    x: Cnf = cnf([[1, 2, 3], [1, 2, 3, -4], [1, 3], [1, 2]])
    assert subclause_reduction(x) == cnf([[1, 2], [1, 3]])


@given(st.from_type(Cnf))
def test_subclause_reduction_results_in_equisatisfiable_clauses(
        cnf_instance: Cnf) -> None:
    assert cnf_pysat_satcheck(cnf_instance) \
        == cnf_pysat_satcheck(subclause_reduction(cnf_instance))
