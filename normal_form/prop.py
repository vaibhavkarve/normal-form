#!/usr/bin/env python3.8
"""Functions for propositional calculus -- conjunction, disjunction and negation."""

import functools as ft

from loguru import logger

from normal_form.cnf import Clause, Cnf, Lit, clause, cnf, neg, tauto_reduce

# Conjunction
# ===========


def literal_and_literal(literal1: Lit, literal2: Lit) -> Cnf:
    """Conjunction of a literal and a literal."""
    return cnf([[literal1], [literal2]])


def clause_and_literal(clause_: Clause, literal: Lit) -> Cnf:
    """Conjunction of a clause and literal."""
    return cnf([clause_, [literal]])


def clause_and_clause(clause1: Clause, clause2: Clause) -> Cnf:
    """Conjunction of a clause and a clause."""
    return cnf([clause1, clause2])


def cnf_and_literal(cnf1: Cnf, literal: Lit) -> Cnf:
    """Conjuncton of a Cnf and a literal."""
    return cnf(cnf1 | {(literal, )})


def cnf_and_clause(cnf1: Cnf, clause_: Clause) -> Cnf:
    """Conjunction of a Cnf and a clause."""
    return cnf(cnf1 | {clause_})


def cnf_and_cnf(cnf1: Cnf, cnf2: Cnf) -> Cnf:
    """Conjunction of a Cnf and a Cnf."""
    return cnf(cnf1 | cnf2)


# Disjunction
# ===========


def literal_or_literal(literal1: Lit, literal2: Lit) -> Clause:
    """Disjunction of a Cnf and a Cnf."""
    return clause([literal1, literal2])


def clause_or_literal(clause_: Clause, literal: Lit) -> Clause:
    """Disjunction of a Cnf and a Cnf."""
    return clause(clause_ | {literal})


def clause_or_clause(clause1: Clause, clause2: Clause) -> Clause:
    """Disjunction of a Cnf and a Cnf."""
    return clause(clause1 | clause2)


def cnf_or_literal(cnf1: Cnf, literal: Lit) -> Cnf:
    """Disjunction of a Cnf and a Cnf."""
    return cnf([clause_or_literal(clause, literal) for clause in cnf1])


def cnf_or_clause(cnf1: Cnf, clause_: Clause) -> Cnf:
    """Disjunction of a Cnf and a Cnf."""
    return cnf([clause_or_clause(clause1, clause_) for clause1 in cnf1])


def cnf_or_cnf(cnf1: Cnf, cnf2: Cnf) -> Cnf:
    """Disjunction of a Cnf and a Cnf."""
    return ft.reduce(cnf_and_cnf, (cnf_or_clause(cnf1, clause) for clause in cnf2))


# Negation
# ========


def neg_clause(clause1: Clause) -> Cnf:
    """Negate a Clause by distributing negation across literals and returning resulting Cnf.

    Example:
        negation of (a ∨ b ∨ ¬ c) = ¬(a ∨ b ∨ ¬ c) = (¬ a ∧ ¬ b ∧ c) : Cnf.

    This function is an almost-involution in the sense that two negations return us back to
    the original clause, but we pass through an intermediate Cnf-instance.
    """
    return cnf(clause([neg(literal)]) for literal in clause1)


def neg_cnf(cnf1: Cnf) -> Cnf:
    """Negate a Cnf by distributing negation across clauses and returning resulting Cnf.

    Example:
        negation of (c₁ ∧ c₂) = ¬(c₁ ∧ c₂) = ¬c₁ ∨ ¬c₂ : Cnf.

    This function is an involution.
    """
    return ft.reduce(cnf_or_cnf, map(neg_clause, cnf1))


if __name__ == '__main__':  # pragma: no cover
    logger.info('Conjunction between two Cnfs:')
    logger.info('>>> cnf_and_cnf(cnf([[1, 2], [3, 4]]), cnf([[-1, 5], [6]]))')
    logger.info(cnf_and_cnf(cnf([[1, 2], [3, 4]]), cnf([[-1, 5], [6]])))
    logger.info('\n')
    logger.info('Disjunction between two Cnfs:')
    logger.info('>>> cnf_or_cnf(cnf([[1, 2], [3, 4]]), cnf([[-1, 5], [6]]))')
    logger.info(cnf_or_cnf(cnf([[1, 2], [3, 4]]), cnf([[-1, 5], [6]])))
    logger.info('>>> tauto_reduce(_)')
    logger.info(tauto_reduce(cnf_or_cnf(cnf([[1, 2], [3, 4]]),
                                        cnf([[-1, 5], [6]]))))
    logger.info('\n')
    logger.info('Negation of a Cnf:')
    logger.info('>>> neg_cnf(cnf([[1, -2], [2, -3]]))')
    logger.info(neg_cnf(cnf([[1, -2], [2, -3]])))
    logger.info('>>> tauto_reduce(_)')
    logger.info(tauto_reduce(neg_cnf(cnf([[1, -2], [2, -3]]))))
