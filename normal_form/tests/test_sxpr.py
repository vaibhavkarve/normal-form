#! /usr/bin/env python3.8

import operator as op
from normal_form.cnf import Cnf
from normal_form.sxpr import AtomicSxpr, SatSxpr, Sxpr


def test_Sxpr() -> None:
    assert Sxpr(lambda x, y: x+y, (1, 2, 3, 4), 0).reduce() == 10
    assert Sxpr(lambda x, y: x+y, (1, 2, 3, 4), 100).reduce() == 110
    assert Sxpr(lambda x, b: x**2 if b else x, (True, True, False, True), 2).reduce() == 256


def test_SatSxpr() -> None:
    # empty arguments
    assert SatSxpr(op.__and__, ()).reduce()
    assert not SatSxpr(op.__or__, ()).reduce()

    # boolean arguments
    assert SatSxpr(op.__and__, (True, True, True)).reduce()
    assert not SatSxpr(op.__and__, (True, True, False)).reduce()
    assert not SatSxpr(op.__and__, (True, False, True)).reduce()
    assert not SatSxpr(op.__and__, (False, True, True)).reduce()

    assert not SatSxpr(op.__or__, (False, False, False)).reduce()
    assert SatSxpr(op.__or__, (True, True, False)).reduce()
    assert SatSxpr(op.__or__, (True, False, True)).reduce()
    assert SatSxpr(op.__or__, (False, True, True)).reduce()
    assert not SatSxpr(op.__or__, (False, False)).reduce()


def test_SatSxpr_at_type_level() -> None:
    complex_sxpr: SatSxpr[Cnf | bool] = AtomicSxpr(op=op.and_, terms=(True, False))
    assert isinstance(complex_sxpr, type(complex_sxpr))
