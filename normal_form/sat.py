#!/usr/bin/env python3.8
"""Functions for sat-checking Cnfs, Graphs, and MHGraphs.

Satisfiability of Cnfs
======================
A Cnf is satisfiable if there exists a truth assignment for each variable in the Cnf
such that on applying the assignment, the Cnf evaluates to True.
This module implements three different sat-solvers:

   1. cnf_bruteforce_satcheck: a brute-force solver.  This solver is easy to
      understand and reason about. It does not have other external
      dependencies. However, it is quite slow.

   2. cnf_pysat_satcheck: using the `pysat` library's Minisat22 solver.  This solver
      calls Minisat v2.2 via the pysat library. It is the fast solver in this list
      but has many external dependencies (because pysat has many dependencies).

   3. cnf_minisat_satcheck: using Minisat v2.2 as a subprocess.  This calls minisat.c
      directly as a subprocess. minisat.c is easy to obtain and install. However,
      creating subprocesses is not a very fast process.

TODO: Add a function for equisatisfiability of Cnfs
"""
# Imports from standard library
import itertools as it
import subprocess
from typing import Iterator, cast

# Imports from third-party modules.
import more_itertools as mit
from loguru import logger
from pysat.solvers import Minisat22  # type: ignore[import]

# Imports from local modules.
from normal_form.cnf import (FALSE_CNF, TRUE_CNF, Assignment, Bool, Cnf, Lit,
                             Variable, absolute_value, assign, cnf, int_repr,
                             lit, lits, tauto_reduce, variable)

# Functions for Checking Satisfiability of Cnfs
# =============================================


def generate_assignments(cnf_instance: Cnf) -> Iterator[Assignment]:
    """Generate all :math:`2^n` truth-assignments for a Cnf with :math:`n` Variables.

    A Cnf's `truth-assignment` will be represented as a dictionary with keys being
    all the Variables that appear in the Cnf and values being Bools.

    Edge cases:

       * ``TRUE``/``FALSE`` Cnfs are treated as having :math:`0` Variables and
         therefore their only corresponding truth-assignment is the empty dictionary.
         In other words, the function returns ``({})``.

       * Any Cnf that can be tautologically reduced to TRUE/FALSE also returns ``({})``.

       * This function cannot distinguish between sat/unsat Cnfs.

    Args:
       cnf_instance (:obj:`Cnf`)

    Return:
       First, tautologically reduce the Cnf. Then, return an Iterator of
       truth-assignment dictionaries with keys being Variables and values being
       Bools.

    """
    cnf_reduced: Cnf
    cnf_reduced = tauto_reduce(cnf_instance)

    lit_set: frozenset[Lit]
    lit_set = lits(cnf_reduced) - {lit(Bool.TRUE), lit(Bool.FALSE)}

    lit_value_set: set[int | Bool] = {absolute_value(literal).value for literal in lit_set}
    assert all(isinstance(value, int) for value in lit_value_set)

    variable_set: set[Variable]
    variable_set = {variable(cast(int, value)) for value in lit_value_set}

    assignment_values: Iterator[tuple[Bool, ...]]
    assignment_values = it.product([Bool.TRUE, Bool.FALSE], repeat=len(variable_set))

    for boolean_tuple in assignment_values:
        yield dict(zip(variable_set, boolean_tuple))


def cnf_bruteforce_satcheck(cnf_instance: Cnf) -> bool:
    """Use brute force to check satisfiability of Cnf.

    .. note::
       Brute-forcing is the most sub-optimal strategy possible. Do not use this function
       on large Cnfs. (Anything more than 6 Variables or 6 Clauses is large.)

    Args:
       cnf_instance (:obj:`Cnf`)

    Return:
       First, tautologically reduce the Cnf. Then. if the Cnf is Satisfiable return
       ``True`` else return ``False``.

    """
    cnf_reduced: Cnf = tauto_reduce(cnf_instance)

    if cnf_reduced == TRUE_CNF:
        return True
    if cnf_reduced == FALSE_CNF:
        return False

    def assigns_cnf_to_true(assignment: Assignment) -> bool:
        return assign(cnf_reduced, assignment) == TRUE_CNF

    # Note: cnf_reduced cannot be TRUE/FALSE, hence all_assignments != ({})
    head: list[Assignment]
    all_assignments: Iterator[Assignment] = generate_assignments(cnf_reduced)
    head, all_assignments = mit.spy(all_assignments)
    assert head != [{}], "Empty assignment generated."

    satisfying_assignments: Iterator[Assignment]
    satisfying_assignments = filter(assigns_cnf_to_true, all_assignments)

    return any(satisfying_assignments)


def cnf_pysat_satcheck(cnf_instance: Cnf) -> bool:
    """Use the `pysat` library's Minisat22 solver to sat-check a Cnf.

    Args:
       cnf_instance (:obj:`Cnf`)

    Return:
       If the Cnf is Satisfiable return ``True`` else return ``False``.

    """
    if cnf_instance == TRUE_CNF:
        return True
    if cnf_instance == FALSE_CNF:
        return False

    try:
        if (result := Minisat22(int_repr(cnf_instance)).solve()) is None:
            raise RuntimeError("Minisat22 returned None as result.")  # pragma: nocover
        assert isinstance(result, bool)
        return result
    except (TypeError, RuntimeError) as exc:
        # The Cnf was probably not in reduced form. Reduce and try again
        cnf_reduced: Cnf = tauto_reduce(cnf_instance)
        if cnf_reduced == cnf_instance:
            raise RuntimeError(
                "Irreducible Cnf not getting solved by Minisat22") from exc  # pragma: nocover
        return cnf_pysat_satcheck(cnf_instance=cnf_reduced)


def cnf_to_dimacs(cnf_instance: Cnf) -> str:
    """Convert a Cnf to DIMACS format.

    The Cnf is tautologically reduced first so as to not contain TRUE or FALSE lits.
    Args:
       cnf_instance (:obj:`Cnf`)

    Return:
       A string which consists of lines. Each line is a Clause of the Cnf ending with
       zero. Each lit in the Clause is written with a space delimiter.

       After tautological reduction, if the Cnf reduced to TRUE or FALSE then return a
       string that will be correctly interpreted as such.

    """
    cnf_reduced: Cnf
    cnf_reduced = tauto_reduce(cnf_instance)

    if cnf_reduced == TRUE_CNF:
        return ''  # A Clause that is always satisfied
    if cnf_reduced == FALSE_CNF:
        return '0'  # A Clause that can never be satisfied

    clause_strs: map[map[str]]
    clause_strs = map(lambda clause: map(str, clause), int_repr(cnf_reduced))

    clause_strs_with_tails: map[str]
    clause_strs_with_tails = map(lambda clause_str: ' '.join(clause_str) + ' 0',
                                 clause_strs)

    return '\n'.join(clause_strs_with_tails)


def cnf_minisat_satcheck(cnf_instance: Cnf) -> bool:
    """Use the `subprocess` library to call minisat.c solver to sat-check a Cnf.

    minisat.c should be correctly installed for this to work.

    Args:
       cnf_instance (:obj:`Cnf`)

    Return:
       If the Cnf is Satisfiable return ``True`` else return ``False``.

    """
    cnf_dimacs: str
    cnf_dimacs = cnf_to_dimacs(cnf_instance)

    output: str = subprocess.run(['minisat', '-rnd-init', '-verb=0'],
                                 input=cnf_dimacs,
                                 text=True,
                                 capture_output=True,
                                 shell=True,
                                 check=False).stdout
    assert output, "Empty output. Check if minisat is installed on your system."
    result: str = output.split()[-1]
    if result == 'SATISFIABLE':
        return True
    if result == 'UNSATISFIABLE':
        return False
    raise RuntimeError('Unexpected output from minisat.', output)   # pragma: no cover


if __name__ == '__main__':  # pragma: no cover
    logger.info('We have several different sat-solvers implemented here.')
    logger.info(">>> cnf_bruteforce_satcheck(cnf([[1, 2], [-1, 2], [1, -2]]))")
    logger.success(cnf_bruteforce_satcheck(cnf([[1, 2], [-1, 2], [1, -2]])))
    logger.info('\n')
    logger.info('An example which is unsatisfiable:')
    logger.info(">>> cnf_pysat_satcheck(cnf([[1, 2], [1, -2], [-1, 2], [-1, -2]]))")
    logger.success(cnf_pysat_satcheck(cnf([[1, 2], [1, -2], [-1, 2], [-1, -2]])))
