#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2023 Beartype authors.
# See "LICENSE" for further details.

'''
**Beartype** :pep:`585` **utility unit tests.**

This submodule unit tests the public API of the private
:mod:`beartype._util.hint.pep.proposal.utilpep585` submodule.
'''

# ....................{ IMPORTS                            }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To raise human-readable test errors, avoid importing from
# package-specific submodules at module scope.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# ....................{ TESTS ~ kind : builtin             }....................
def test_is_hint_pep585_builtin(hints_pep_meta) -> None:
    '''
    Test the
    :func:`beartype._util.hint.pep.proposal.utilpep585.is_hint_pep585_builtin`
    function.

    Parameters
    ----------
    hints_pep_meta : List[beartype_test.a00_unit.data.hint.util.data_hintmetacls.HintPepMetadata]
        List of type hint metadata describing sample type hints exercising edge
        cases in the :mod:`beartype` codebase.
    '''

    # Defer test-specific imports.
    from beartype._util.hint.pep.proposal.utilpep585 import (
        is_hint_pep585_builtin)

    # Assert this tester accepts only PEP 585-compliant type hints.
    for hint_pep_meta in hints_pep_meta:
        assert is_hint_pep585_builtin(hint_pep_meta.hint) is (
            hint_pep_meta.is_pep585_builtin)

# ....................{ TESTS ~ kind : generic            }....................
def test_is_hint_pep585_generic(hints_pep_meta) -> None:
    '''
    Test the
    :func:`beartype._util.hint.pep.proposal.utilpep585.is_hint_pep585_generic`
    function.

    Parameters
    ----------
    hints_pep_meta : List[beartype_test.a00_unit.data.hint.util.data_hintmetacls.HintPepMetadata]
        List of type hint metadata describing sample type hints exercising edge
        cases in the :mod:`beartype` codebase.
    '''

    # Defer test-specific imports.
    from beartype._util.hint.pep.proposal.utilpep585 import (
        is_hint_pep585_generic)

    # Assert this tester accepts only PEP 585-compliant generics.
    for hint_pep_meta in hints_pep_meta:
        assert is_hint_pep585_generic(hint_pep_meta.hint) is (
            hint_pep_meta.is_pep585_generic)


def test_get_hint_pep585_generic_typevars(hints_pep_meta) -> None:
    '''
    Test the
    :func:`beartype._util.hint.pep.proposal.utilpep585.get_hint_pep585_generic_typevars`
    function.

    Parameters
    ----------
    hints_pep_meta : List[beartype_test.a00_unit.data.hint.util.data_hintmetacls.HintPepMetadata]
        List of type hint metadata describing sample type hints exercising edge
        cases in the :mod:`beartype` codebase.
    '''

    # Defer test-specific imports.
    from beartype.roar import BeartypeDecorHintPep585Exception
    from beartype._util.hint.pep.proposal.utilpep585 import (
        get_hint_pep585_generic_typevars)
    from pytest import raises

    # Assert this getter...
    for hint_pep_meta in hints_pep_meta:
        # If this hint is a PEP 585-compliant generic...
        if hint_pep_meta.is_pep585_generic:
            # Tuple of all tupe variables returned by this function.
            hint_pep_typevars = get_hint_pep585_generic_typevars(
                hint_pep_meta.hint)

            # Returns one or more type variables for typevared PEP
            # 585-compliant generics.
            if hint_pep_meta.is_typevars:
                assert isinstance(hint_pep_typevars, tuple)
                assert hint_pep_typevars
            # *NO* type variables for untypevared PEP 585-compliant generics.
            else:
                assert hint_pep_typevars == ()
        # Raises an exception for objects *NOT* PEP 585-compliant generics.
        else:
            with raises(BeartypeDecorHintPep585Exception):
                get_hint_pep585_generic_typevars(hint_pep_meta.hint)
