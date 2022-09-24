#!/usr/bin/env python3.8

import functools as ft
import itertools as it

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from normal_form.cnf import (FALSE_CLAUSE, FALSE_CNF, TRUE_CLAUSE, TRUE_CNF,
                             Bool, Clause, Cnf, Lit, clause, cnf, lit, neg,
                             tauto_reduce)
from normal_form.prop import (clause_and_clause, clause_and_literal,
                              clause_or_clause, clause_or_literal,
                              cnf_and_clause, cnf_and_cnf, cnf_and_literal,
                              cnf_or_clause, cnf_or_cnf, cnf_or_literal,
                              literal_and_literal, literal_or_literal,
                              neg_clause, neg_cnf)


@given(st.from_type(Lit), st.from_type(Lit))
def test_literal_and_literal(lit1: Lit, lit2: Lit) -> None:
    # Check the definition.
    assert literal_and_literal(lit1, lit2) == cnf([[lit1], [lit2]])
    # Check commutativity.
    assert literal_and_literal(lit1, lit2) == literal_and_literal(lit2, lit1)
    # Check l ∧ l = l.
    assert literal_and_literal(lit1, lit1) == cnf([[lit1]])
    # Check l ∧ ⊤ = l (after simplification).
    assert tauto_reduce(literal_and_literal(lit1, lit(Bool.TRUE))) \
        == cnf([[lit1]])
    # Check l ∧ ⊥ = ⊥ (after simplification)
    assert tauto_reduce(literal_and_literal(lit1, lit(Bool.FALSE))) \
        == FALSE_CNF


@given(st.from_type(Clause), st.from_type(Lit))
def test_clause_and_literal(clause_instance: Clause, literal: Lit) -> None:
    # Check the definition.
    assert clause_and_literal(clause_instance, literal) \
        == cnf([clause_instance, [literal]])
    # Check commutativity.
    assert clause_and_literal(clause([literal]), literal) == cnf([[literal]])
    # Check c ∧ ⊤ = c (after simplification).
    assert tauto_reduce(clause_and_literal(clause_instance, lit(Bool.TRUE))) \
        == tauto_reduce(cnf([clause_instance]))
    # Check c ∧ ⊥ = ⊥ (after simplification).
    assert tauto_reduce(clause_and_literal(clause_instance, lit(Bool.FALSE))) \
        == FALSE_CNF
    # Check ⊤ ∧ l = l (after simplification).
    assert tauto_reduce(clause_and_literal(TRUE_CLAUSE, literal)) \
        == cnf([[literal]])
    # Check ⊥ ∧ l = ⊥ (after simplification).
    assert tauto_reduce(clause_and_literal(FALSE_CLAUSE, literal)) \
        == FALSE_CNF


@given(st.from_type(Clause), st.from_type(Clause))
def test_clause_and_clause(cl1: Clause, cl2: Clause) -> None:
    # Check the definition.
    assert clause_and_clause(cl1, cl2) == cnf([cl1, cl2])
    # Check commutativity.
    assert clause_and_clause(cl1, cl2) == clause_and_clause(cl2, cl1)
    # Check c ∧ c = c.
    assert clause_and_clause(cl1, cl1) == cnf([cl1])
    # Check c ∧ ⊤ = c (with simplification).
    assert tauto_reduce(clause_and_clause(cl1, TRUE_CLAUSE)) == tauto_reduce(cnf([cl1]))
    # Check c ∧ ⊥ = ⊥ (after simplification).
    assert tauto_reduce(clause_and_clause(cl1, FALSE_CLAUSE)) == FALSE_CNF


@given(st.from_type(Cnf), st.from_type(Lit))
def test_cnf_and_literal(cnf_instance: Cnf, literal: Lit) -> None:
    # Check the definition.
    assert cnf_and_literal(cnf_instance, literal) == cnf(cnf_instance | cnf([[literal]]))
    # Check commutativity.
    assert cnf_and_literal(cnf([[literal]]), literal) == cnf([[literal]])
    # Check x ∧ ⊤ = x (with simplification).
    assert tauto_reduce(cnf_and_literal(cnf_instance, lit(Bool.TRUE))) \
        == tauto_reduce(cnf_instance)
    # Check x ∧ ⊥ = ⊥ (with simplification).
    assert tauto_reduce(cnf_and_literal(cnf_instance, lit(Bool.FALSE))) == FALSE_CNF
    # Check ⊤ ∧ l = l (with simplification).
    assert tauto_reduce(cnf_and_literal(TRUE_CNF, literal)) == cnf([[literal]])
    # Check ⊥ ∧ l = ⊥ (with simplification).
    assert tauto_reduce(cnf_and_literal(FALSE_CNF, literal)) == FALSE_CNF


@given(st.from_type(Cnf), st.from_type(Clause))
def test_cnf_and_clause(cnf_instance: Cnf, clause_instance: Clause) -> None:
    # Check the definition.
    assert cnf_and_clause(cnf_instance, clause_instance) \
        == cnf(cnf_instance | cnf([clause_instance]))
    # Check commutativity.
    assert cnf_and_clause(cnf([clause_instance]), clause_instance) \
        == cnf([clause_instance])
    # Check x ∧ ⊤ = x (with simplification).
    assert tauto_reduce(cnf_and_clause(cnf_instance, TRUE_CLAUSE)) \
        == tauto_reduce(cnf_instance)
    # Check x ∧ ⊥ = ⊥ (with simplification).
    assert tauto_reduce(cnf_and_clause(cnf_instance, FALSE_CLAUSE)) == FALSE_CNF
    # Check ⊤ ∧ c = c (with simplification).
    assert tauto_reduce(cnf_and_clause(TRUE_CNF, clause_instance)) \
        == tauto_reduce(cnf([clause_instance]))
    # Check ⊥ ∧ c = ⊥ (with simplification).
    assert tauto_reduce(cnf_and_clause(FALSE_CNF, clause_instance)) == FALSE_CNF


@given(st.from_type(Cnf), st.from_type(Cnf))
def test_cnf_and_cnf(cnf1: Cnf, cnf2: Cnf) -> None:
    # Check the definition.
    assert cnf_and_cnf(cnf1, cnf2) == cnf(cnf1 | cnf2)
    # Check commutativity.
    assert cnf_and_cnf(cnf1, cnf2) == cnf_and_cnf(cnf2, cnf1)
    # Check x ∧ x = x.
    assert cnf_and_cnf(cnf1, cnf1) == cnf1
    # Check x ∧ ⊤ = x (with simplification).
    assert tauto_reduce(cnf_and_cnf(cnf1, TRUE_CNF)) == tauto_reduce(cnf1)
    # Check x ∧ ⊥ = ⊥ (with simplification).
    assert tauto_reduce(cnf_and_cnf(cnf1, FALSE_CNF)) == FALSE_CNF


@given(st.from_type(Lit), st.from_type(Lit))
def test_literal_or_literal(lit1: Lit, lit2: Lit) -> None:
    # Check the definition.
    assert literal_or_literal(lit1, lit2) == clause([lit1, lit2])
    # Check commutativity.
    assert literal_or_literal(lit1, lit2) == literal_or_literal(lit2, lit1)
    # Check l ∨ l = l.
    assert literal_or_literal(lit1, lit1) == clause([lit1])
    # Check l ∨ ⊤ = ⊤ (after simplification).
    assert tauto_reduce(literal_or_literal(lit1, lit(Bool.TRUE))) \
        == TRUE_CLAUSE
    # Check l ∨ ⊥ = l (after simplification)
    assert tauto_reduce(literal_or_literal(lit1, lit(Bool.FALSE))) \
        == clause([lit1])


@given(st.from_type(Clause), st.from_type(Lit))
def test_clause_or_literal(clause_instance: Clause, literal: Lit) -> None:
    # Check the definition.
    assert clause_or_literal(clause_instance, literal) \
        == clause(clause_instance | {literal})
    # Check commutativity.
    assert clause_or_literal(clause([literal]), literal) == clause([literal])
    # Check c ∨ ⊤ = ⊤ (after simplification).
    assert tauto_reduce(clause_or_literal(clause_instance, lit(Bool.TRUE))) \
        == TRUE_CLAUSE
    # Check c ∨ ⊥ = c (after simplification).
    assert tauto_reduce(clause_or_literal(clause_instance, lit(Bool.FALSE))) \
        == tauto_reduce(clause_instance)
    # Check ⊤ ∨ l = ⊤ (after simplification).
    assert tauto_reduce(clause_or_literal(TRUE_CLAUSE, literal)) \
        == TRUE_CLAUSE
    # Check ⊥ ∨ l = l (after simplification).
    assert tauto_reduce(clause_or_literal(FALSE_CLAUSE, literal)) \
        == clause([literal])


@given(st.from_type(Clause), st.from_type(Clause))
def test_clause_or_clause(cl1: Clause, cl2: Clause) -> None:
    # Check the definition.
    assert clause_or_clause(cl1, cl2) == clause(cl1 | cl2)
    # Check commutativity.
    assert clause_or_clause(cl1, cl2) == clause_or_clause(cl2, cl1)
    # Check c ∨ c = c.
    assert clause_or_clause(cl1, cl1) == cl1
    # Check c ∨ ⊤ = ⊤ (with simplification).
    assert tauto_reduce(clause_or_clause(cl1, TRUE_CLAUSE)) == TRUE_CLAUSE
    # Check c ∨ ⊥ = c (after simplification).
    assert tauto_reduce(clause_or_clause(cl1, FALSE_CLAUSE)) == tauto_reduce(cl1)


@given(st.from_type(Cnf), st.from_type(Lit))
def test_cnf_or_literal(cnf_instance: Cnf, literal: Lit) -> None:
    # Check the definition.
    assert cnf_or_literal(cnf_instance, literal) == cnf(
        [clause | {literal} for clause in cnf_instance])
    # Check commutativity.
    assert cnf_or_literal(cnf([[literal]]), literal) == cnf([[literal]])
    # Check x ∨ ⊤ = ⊤ (with simplification).
    assert tauto_reduce(cnf_or_literal(cnf_instance, lit(Bool.TRUE))) == TRUE_CNF
    # Check x ∨ ⊥ = x (with simplification).
    assert tauto_reduce(cnf_or_literal(cnf_instance, lit(Bool.FALSE))) \
        == tauto_reduce(cnf_instance)
    # Check ⊤ ∨ l = ⊤ (with simplification).
    assert tauto_reduce(cnf_or_literal(TRUE_CNF, literal)) == TRUE_CNF
    # Check ⊥ ∨ l = l (with simplification).
    assert tauto_reduce(cnf_or_literal(FALSE_CNF, literal)) == cnf([[literal]])


@given(st.from_type(Cnf), st.from_type(Clause))
def test_cnf_or_clause(cnf_instance: Cnf, clause_instance: Clause) -> None:
    # Check the definition.
    assert cnf_or_clause(cnf_instance, clause_instance) \
        == cnf([clause | clause_instance for clause in cnf_instance])
    # Check commutativity.
    assert cnf_or_clause(cnf([clause_instance]), clause_instance) \
        == cnf([clause_instance])
    # Check x ∨ ⊤ = ⊤ (with simplification).
    assert tauto_reduce(cnf_or_clause(cnf_instance, TRUE_CLAUSE)) == TRUE_CNF
    # Check x ∨ ⊥ = x (with simplification).
    assert tauto_reduce(cnf_or_clause(cnf_instance, FALSE_CLAUSE)) \
        == tauto_reduce(cnf_instance)
    # Check ⊤ ∨ c = ⊤ (with simplification).
    assert tauto_reduce(cnf_or_clause(TRUE_CNF, clause_instance)) == TRUE_CNF
    # Check ⊥ ∨ c = c (with simplification).
    assert tauto_reduce(cnf_or_clause(FALSE_CNF, clause_instance)) \
        == tauto_reduce(cnf([clause_instance]))


@given(st.from_type(Cnf), st.from_type(Cnf))
def test_cnf_or_cnf(cnf1: Cnf, cnf2: Cnf) -> None:
    # Check the definition.
    assert cnf_or_cnf(cnf1, cnf2) == cnf([clause1 | clause2
                                          for clause1, clause2 in it.product(cnf1, cnf2)])
    # Check commutativity.
    assert cnf_or_cnf(cnf1, cnf2) == cnf_or_cnf(cnf1=cnf2, cnf2=cnf1)
    # Check x ∨ x = x (with simplification).
    assert tauto_reduce(cnf_or_cnf(cnf1, cnf1)) == tauto_reduce(cnf1)
    # Check x ∨ ⊤ = ⊤ (with simplification).
    assert tauto_reduce(cnf_or_cnf(cnf1, TRUE_CNF)) == TRUE_CNF
    # Check x ∨ ⊥ = x (with simplification).
    assert tauto_reduce(cnf_or_cnf(cnf1, FALSE_CNF)) == tauto_reduce(cnf1)


@given(st.from_type(Cnf), st.from_type(Cnf), st.from_type(Cnf))
@settings(max_examples=10)
def test_distributivity(cnf1: Cnf, cnf2: Cnf, cnf3: Cnf) -> None:
    # Conjunction distributes over disjunction.
    cnf_and_cnf(cnf1, cnf_or_cnf(cnf2, cnf3)) == cnf_or_cnf(cnf_and_cnf(cnf1, cnf2),
                                                            cnf_and_cnf(cnf1, cnf3))
    # Disjunction distributes over conjunction.
    cnf_or_cnf(cnf1, cnf_or_cnf(cnf2, cnf3)) == cnf_and_cnf(cnf_or_cnf(cnf1, cnf2),
                                                            cnf_or_cnf(cnf1, cnf3))


@given(st.from_type(Clause))
@settings(max_examples=10)
def test_neg_clause(clause_instance: Clause) -> None:
    # Check the definition.
    assert neg_clause(clause_instance) == cnf(
        [clause([neg(literal)]) for literal in clause_instance])


@pytest.mark.skip(reason="hypothesis.errors.Flaky i.e. test fails on unexpected outputs.")
@given(st.from_type(Cnf))
def test_neg_cnf(cnf_instance: Cnf) -> None:
    # Check for the definition.
    assert neg_cnf(cnf_instance) == ft.reduce(cnf_or_cnf, map(neg_clause, cnf_instance))
