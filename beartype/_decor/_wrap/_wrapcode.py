#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2023 Beartype authors.
# See "LICENSE" for further details.

'''
**Beartype type-checking wrapper function code factories** (i.e., low-level
callables dynamically generating pure-Python code snippets type-checking
parameters and return values of :mod:`beartype`-decorated callables against the
PEP-compliant type hints annotating those callables).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from beartype._check.checkmagic import ARG_NAME_GETRANDBITS
from beartype._check.code.codemake import make_check_expr
from beartype._conf.confcls import BeartypeConf
from beartype._data.hint.datahinttyping import (
    CodeGenerated,
    TypeStack,
)
from beartype._decor._wrap.wrapsnip import (
    CODE_HINT_ROOT_PREFIX,
    CODE_HINT_ROOT_SUFFIX,
    CODE_HINT_ROOT_SUFFIX_CLS_STACK,
    CODE_HINT_ROOT_SUFFIX_RANDOM_INT,
)
from beartype._util.cache.utilcachecall import callable_cached

# ....................{ MAKERS                             }....................
@callable_cached
def make_func_wrapper_code(
    hint: object,
    conf: BeartypeConf,
    cls_stack: TypeStack,
) -> CodeGenerated:
    '''
    **Type-checking wrapper function code factory** (i.e., low-level callable
    dynamically generating a pure-Python code snippet type-checking the
    previously localized parameter or return value annotated by the passed
    PEP-compliant type hint against that hint of the current
    :mod:`beartype`-decorated callable).

    This code factory is memoized for efficiency.

    Parameters
    ----------
    hint : object
        PEP-compliant type hint to be type-checked.
    conf : BeartypeConf
        **Beartype configuration** (i.e., self-caching dataclass encapsulating
        all settings configuring type-checking for the passed object).
    cls_stack : TypeStack
        **Type stack** (i.e., either a tuple of the one or more
        :func:`beartype.beartype`-decorated classes lexically containing the
        class variable or method annotated by this hint *or* :data:`None`).

    Returns
    ----------
    CodeGenerated
        Tuple containing the Python code snippet dynamically generated by this
        code factory and metadata describing that code. See the
        :attr:`beartype._data.hint.datahinttyping.CodeGenerated` type hint for details.

    Raises
    ----------
    All exceptions raised by the lower-level :func:`make_check_expr` factory.

    Warns
    ----------
    All warnings emitted by the lower-level :func:`make_check_expr` factory.

    See Also
    ----------
    :func:`make_check_expr`
        Further details.
    '''

    # Python code snippet comprising a single boolean expression type-checking
    # an arbitrary object against this hint.
    (
        func_wrapper_code_expr,
        func_wrapper_scope,
        hint_forwardrefs_class_basename,
    ) = make_check_expr(hint, conf, cls_stack)

    # Code snippet passing the current class stack if needed to type-check this
    # type hint, defaulting to *NOT* passing this.
    arg_cls_stack = CODE_HINT_ROOT_SUFFIX_CLS_STACK if cls_stack else ''

    # Code snippet passing the value of the random integer previously generated
    # for the current call to the exception-handling function call embedded in
    # the "CODE_HINT_ROOT_SUFFIX" snippet, defaulting to *NOT* passing this.
    arg_random_int = (
        CODE_HINT_ROOT_SUFFIX_RANDOM_INT
        if ARG_NAME_GETRANDBITS in func_wrapper_scope else
        ''
    )

    #FIXME: [SPEED] Optimize the following two string munging operations into a
    #single string-munging operation resembling:
    #    func_wrapper_code = CODE_HINT_ROOT.format(
    #        check_expr=func_wrapper_code_expr,
    #        random_int_if_any=arg_random_int
    #    )
    #
    #Then define "CODE_HINT_ROOT" in the "wrapsnip" submodule to resemble:
    #    CODE_HINT_ROOT = (
    #        f'{CODE_HINT_ROOT_PREFIX}{{check_expr}}'
    #        f'{CODE_HINT_ROOT_SUFFIX}'
    #    )

    # Suffix this code by a Python code snippet raising a human-readable
    # exception when the root pith violates the root type hint.
    func_wrapper_code_suffix = CODE_HINT_ROOT_SUFFIX.format(
        arg_cls_stack=arg_cls_stack,
        arg_random_int=arg_random_int,
    )

    # Python code snippet type-checking the root pith against the root hint.
    func_wrapper_code = (
        f'{CODE_HINT_ROOT_PREFIX}'
        f'{func_wrapper_code_expr}'
        f'{func_wrapper_code_suffix}'
    )

    # Return all metadata required by higher-level callers.
    return (
        func_wrapper_code,
        func_wrapper_scope,
        hint_forwardrefs_class_basename,
    )
