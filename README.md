**A Python package for working with Conjunctive Normal Form (CNFs) and Boolean Satisfiability (SAT)**

<a href="https://img.shields.io/github/license/vaibhavkarve/normal-form?style=flat-square"> <img src="https://img.shields.io/github/license/vaibhavkarve/normal-form?style=flat-square" alt="License"> </a>
<a href="https://img.shields.io/badge/Python-v3.10-blue?style=flat-square"> <img src="https://img.shields.io/badge/Python-v3.10-blue?style=flat-square" alt="Python:v3.10"> </a>

This Python package is brought to you by [Vaibhav Karve](https://vaibhavkarve.github.io) and [Anil N. Hirani](https://faculty.math.illinois.edu/~hirani/), Department of Mathematics, University of Illinois at Urbana-Champaign.

`normal-form` recognizes variables, literals, clauses, and CNFs. The package implements an interface to easily construct CNFs and SAT-check them via third-part libraries [MINISAT](http://minisat.se/) and [PySAT](https://pysathq.github.io/).

This package is written in Python v3.10, and is publicly available under the [GNU-GPL-v3.0 license](https://github.com/vaibhavkarve/normal-form/blob/main/LICENSE). It is set to be released on the [Python Packaging Index](https://pypi.org/) as an open-source scientific package written in the literate programming style. We specifically chose to write this package as a literate program, despite the verbosity of this style, with the goal to create reproducible computational research.


# Installation and usage

To get started on using this package,

1.  Istall Python 3.10 or higher.
2.  `python3.10 -m pip install normal-form`
3.  Use it in a python script (or interactive REPL) as &#x2013;
    
    ```python
    from normal_form import cnf
    from normal_form import sat
    
    # This is the CNF (a ∨ b ∨ ¬c) ∧ (¬b ∨ c ∨ ¬d) ∧ (¬a ∨ d).
    x1: cnf.Cnf = cnf.cnf([[1, 2, -3], [-2, 3, -4], [-1, 4]])
    
    sat_x1: bool = sat.cnf_bruteforce_satcheck(x1)
    print(sat_x1)  # prints: True because x1 is satisfiable.
    ```


# Overview of modules

The package consists of the following modules.

| **Modules that act on Cnfs**      |                                                                                     |
| [`cnf.py`](cnf)                   | Constructors and functions for sentences in conjunctive normal form                 |
| [`cnf_simplify.py`](cnf_simplify) | Functions for simplifying Cnfs, for example (a∨b∨c) ∧ (a∨b∨&not; c) ⇝ (a ∨ b)       |
| [`prop.py`](prop)                 | Functions for propositional calculus &#x2013; conjunction, disjunction and negation |
| **Modules concerning SAT**        |                                                                                     |
| [`sat.py`](sat)                   | Functions for sat-checking Cnfs                                                     |
| [`sxpr.py`](sxpr)                 | Functions for working with s-expressions                                            |
| **Test suite**                    |                                                                                     |
| `tests/*`                         | Unit- and property-based tests for each module                                      |


# Algorithms

Currently, `normal-form` implements the following algorithms &#x2013;

-   For formulae in conjunctive normal forms (CNFs), it implements variables, literals, clauses, Boolean formulae, and truth-assignments. It includes an API for reading, parsing and defining new instances.

-   For satisfiability of CNFs, it contains a bruteforce algorithm, an implementation that uses the open-source sat-solver [PySAT](https://pysathq.github.io/), and an implementation using the [MiniSAT](http://minisat.se/) solver.


# Principles

`normal-form` has been written in the functional-programming style with the following principles in mind &#x2013;

-   Avoid classes as much as possible. Prefer defining functions instead.

-   Write small functions and then compose/map/filter them to create more complex functions.

-   Use lazy evaluation strategy whenever possible (using the [itertools](https://docs.python.org/3/library/itertools.html) library).

-   Add type hints wherever possible (checked using the [mypy](https://mypy.readthedocs.io/en/stable/) static type-checker).

-   Add unit-tests for each function (checked using the [pytest](https://docs.pytest.org/en/latest/) framework). Further, add property-based testing wherever possible (using the [hypothesis](https://hypothesis.readthedocs.io) framework).