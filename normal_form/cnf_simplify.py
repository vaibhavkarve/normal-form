#!/usr/bin/env python3.8
"""Functions for simplifying Cnfs, particularly (a∨b∨c) ∧ (a∨b∨¬c) to (a∨b).

This simplification is traditionally handled by the Quine–McCluskey
algorithm. But for our simple use-case, this might be over-engineered.

Instead we implement our own functions for making this simplification.

"""
import itertools as it

from normal_form import cnf


def absolute_literals_of_clause(clause: cnf.Clause) -> set[cnf.Lit]:
    """Return the set of all absolute-values of all literals in a clause, .

    absolute_literals_of_clause = set ∘ map(cnf.absolute_value, __)

    """
    return {cnf.absolute_value(literal) for literal in clause}


def differing_lits(clause1: cnf.Clause, clause2: cnf.Clause) -> frozenset[cnf.Lit]:
    """Give a set of literals that two clauses differ on.

    This returns a set that can give us twice the Hamming distance between
    clauses. Assume that the clauses have the same image under `hedge_of_clause`. If
    not, raise an AssertionError.

    Quick way to compute set of distinct lits is to calculate the symmetric
    difference between them (using the ^ operator).

    ∀ c : cnf.Clause,
       differing_lits(c, c) = ∅
    ∀ c d : cnf.Clause,
       differing_lits(c, d) = differing_lits(d, c)

    """
    return clause1 ^ clause2


def equivalent_smaller_clause(clause1: cnf.Clause, clause2: cnf.Clause) -> cnf.Clause:
    """Given clauses that are distance 1 apart, return smaller equiv. clause.

    The smaller equivalent clause is given by the intersection of the two clauses.
    This is computed using the `&` operator.

    """
    assert len(differing_lits(clause1, clause2)) == 2, 'Hamming distance should be 1.'

    equiv_clause: cnf.Clause = cnf.clause(clause1 & clause2)
    assert len(equiv_clause) == len(clause1) - 1
    return equiv_clause


def reduce_distance_one_clauses(cnf_instance: cnf.Cnf) -> cnf.Cnf:
    """Reduce all clauses in the the

    The problem this function is trying to solve is known to be NP-hard. This is an
    inefficient solution to this problem. Do not apply it to Cnfs with more than 5
    variables.

    reduce_cnf = ungroup_clauses_to_cnf ∘ reduce_all_groups ∘ group_clauses_by_edge
    """
    for clause1, clause2 in it.combinations(cnf_instance, 2):
        var_set1: set[cnf.Lit] = absolute_literals_of_clause(clause1)
        var_set2: set[cnf.Lit] = absolute_literals_of_clause(clause2)
        if var_set1 == var_set2 and len(differing_lits(clause1, clause2)) == 2:
            # Hamming distance in clauses = 1
            reduced_cnf = cnf_instance - {clause1, clause2}
            reduced_cnf = reduced_cnf | {equivalent_smaller_clause(clause1, clause2)}
            return reduce_distance_one_clauses(cnf.cnf(reduced_cnf))
    return cnf_instance


def subclause_reduction(cnf_instance: cnf.Cnf) -> cnf.Cnf:
    """Replace the conjunction of two clauses with the smaller clause.

    If c₁ c₂ : cnf.Clause, we sat the c₁ ≪ c₂ if every literal of c₁ is in c₂.

    Replace c₁ ∧ c₂ with c₁ whenever c₁ ≪ c₂.
    Perform action recursively.
    """
    for clause1, clause2 in it.permutations(cnf_instance, 2):
        if clause1 <= clause2:
            new_cnf: cnf.Cnf = cnf.cnf(cnf_instance - {clause2})
            return subclause_reduction(new_cnf)
    return cnf_instance


def reduce_cnf(cnf_instance: cnf.Cnf) -> cnf.Cnf:
    """Reduce distance=1 as well as subclauses."""
    return subclause_reduction(reduce_distance_one_clauses(cnf_instance))


if __name__ == '__main__':  # pragma: no cover
    x: cnf.Cnf = cnf.cnf([[1, 2, -3], [1, 2, 3], [-1, -2, 3], [4, 5], [4, 5, -6]])
    print(reduce_cnf(x))
