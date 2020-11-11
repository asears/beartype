#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright (c) 2014-2020 Cecil Curry.
# See "LICENSE" for further details.

'''
**Beartype decorator PEP-compliant code snippets.**

This private submodule *only* defines **PEP-compliant code snippets** (i.e.,
triple-quoted pure-Python code constants formatted and concatenated together
into wrapper functions implementing type-checking for decorated callables
annotated by PEP-compliant type hints).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ TODO                              }....................
#FIXME: Refactor to leverage f-strings after dropping Python 3.5 support,
#which are the optimal means of performing string formatting.

# ....................{ IMPORTS                           }....................
from beartype._decor._code.codemain import (
    PARAM_NAME_FUNC,
    PARAM_NAME_TYPISTRY,
)
from inspect import Parameter

# ....................{ PITH                              }....................
PEP_CODE_PITH_ASSIGN_EXPR = '''{pith_curr_assigned_expr} := {pith_curr_expr}'''
'''
Python >= 3.8-specific assignment expression assigning the full Python
expression yielding the value of the current pith to a unique local variable,
enabling PEP-compliant child hints to obtain this pith via this efficient
variable rather than via this inefficient full Python expression.
'''


PEP_CODE_PITH_NAME_PREFIX = '__beartype_pith_'
'''
Substring prefixing all local variables providing a **pith** (i.e., either the
current parameter or return value *or* item contained the current parameter or
return value being type-checked by the current call).
'''

# ....................{ PITH ~ root                       }....................
PEP_CODE_PITH_ROOT_NAME = f'{PEP_CODE_PITH_NAME_PREFIX}0'
'''
Name of the local variable providing the **root pith** (i.e., value of the
current parameter or return value being type-checked by the current call).
'''


PEP_CODE_PITH_ROOT_PARAM_NAME_PLACEHOLDER = '?|PITH_ROOT_NAME`^'
'''
Placeholder source substring to be globally replaced by the **root pith name**
(i.e., name of the current parameter if called by the
:func:`pep_code_check_param` function *or* ``return`` if called by the
:func:`pep_code_check_return` function) in the parameter- and return-agnostic
code generated by the memoized :func:`pep_code_check_hint` function.

See Also
----------
:attr:`beartype._decor._code._pep._pephint.pep_code_check_hint`
:attr:`beartype._util.cache.utilcacheerror.EXCEPTION_CACHED_PLACEHOLDER`
    Related commentary.
'''

# ....................{ PARAM                             }....................
#FIXME: Refactor to leverage f-strings after dropping Python 3.5 support,
#which are the optimal means of performing string formatting.
PARAM_KIND_TO_PEP_CODE_GET = {
    # Snippet localizing any positional or keyword parameter as follows:
    #
    # * If this parameter's 0-based index (in the parameter list of the
    #   decorated callable's signature) does *NOT* exceed the number of
    #   positional parameters passed to the wrapper function, localize this
    #   positional parameter from the wrapper's variadic "*args" tuple.
    # * Else if this parameter's name is in the dictionary of keyword
    #   parameters passed to the wrapper function, localize this keyword
    #   parameter from the wrapper's variadic "*kwargs" tuple.
    # * Else, this parameter is unpassed. In this case, localize this parameter
    #   as a placeholder value guaranteed to *NEVER* be passed to any wrapper
    #   function: the private "__beartypistry" singleton passed to this wrapper
    #   function as a hidden default parameter and thus accessible here. While
    #   we could pass a "__beartype_sentinel" parameter to all wrapper
    #   functions defaulting to "object()" and then use that here instead,
    #   doing so would slightly reduce efficiency for no tangible gain. *shrug*
    Parameter.POSITIONAL_OR_KEYWORD: f'''
    # Localize this positional or keyword parameter if passed *OR* to the
    # sentinel value "__beartypistry" guaranteed to never be passed otherwise.
    {PEP_CODE_PITH_ROOT_NAME} = (
        args[{{arg_index}}] if __beartype_args_len > {{arg_index}} else
        kwargs.get({{arg_name!r}}, {PARAM_NAME_TYPISTRY})
    )

    # If this parameter was passed...
    if {PEP_CODE_PITH_ROOT_NAME} is not {PARAM_NAME_TYPISTRY}:''',

    # Snippet localizing any keyword-only parameter (e.g., "*, kwarg") by
    # lookup in the wrapper's variadic "**kwargs" dictionary. (See above.)
    Parameter.KEYWORD_ONLY: f'''
    # Localize this keyword-only parameter if passed *OR* to the sentinel value
    # "__beartypistry" guaranteed to never be passed otherwise.
    {PEP_CODE_PITH_ROOT_NAME} = kwargs.get({{arg_name!r}}, {PARAM_NAME_TYPISTRY})

    # If this parameter was passed...
    if {PEP_CODE_PITH_ROOT_NAME} is not {PARAM_NAME_TYPISTRY}:''',

    # Snippet iteratively localizing all variadic positional parameters.
    Parameter.VAR_POSITIONAL: f'''
    # For all passed positional variadic parameters...
    for {PEP_CODE_PITH_ROOT_NAME} in args[{{arg_index!r}}:]:''',
}
'''
Dictionary mapping from the type of each callable parameter supported by the
:func:`beartype.beartype` decorator to a PEP-compliant code snippet localizing
that callable's next parameter to be type-checked.
'''

# ....................{ RETURN                            }....................
PEP_CODE_CHECK_RETURN_PREFIX = f'''
    # Call this function with all passed parameters and localize the value
    # returned from this call.
    {PEP_CODE_PITH_ROOT_NAME} = {PARAM_NAME_FUNC}(*args, **kwargs)

    # Noop required to artifically increase indentation level. Note that
    # CPython implicitly optimizes this conditional away - which is nice.
    if True:'''
'''
PEP-compliant code snippet calling the decorated callable and localizing the
value returned by that call.

Note that this snippet intentionally terminates on a line containing only the
``(`` character, enabling subsequent type-checking code to effectively ignore
indentation level and thus uniformly operate on both:

* Parameters localized via values of the :data:`PARAM_KIND_TO_PEP_CODE_GET`
  dictionary.
* Return values localized via this sippet.

See Also
----------
https://stackoverflow.com/a/18124151/2809027
    Bytecode disassembly demonstrating that CPython optimizes away the spurious
   ``if True:`` conditional hardcoded into this snippet.
'''


PEP_CODE_CHECK_RETURN_SUFFIX = f'''
    return {PEP_CODE_PITH_ROOT_NAME}'''
'''
PEP-compliant code snippet returning from the wrapper function the successfully
type-checked value returned from the decorated callable.

Note that this snippet intentionally terminates on a line containing only the
``)`` character, which closes the corresponding character terminating the
:data:`PEP_CODE_GET_RETURN` snippet.
'''

# ....................{ RETURN ~ noreturn                 }....................
PEP484_CODE_CHECK_NORETURN = f'''
    # Call this function with all passed parameters and localize the value
    # returned from this call.
    {PEP_CODE_PITH_ROOT_NAME} = {PARAM_NAME_FUNC}(*args, **kwargs)

    # Since this function annotated by "typing.NoReturn" successfully returned
    # a value rather than raising an exception or halting the active Python
    # interpreter, unconditionally raise an exception.
    __beartype_raise_pep_call_exception(
        func={PARAM_NAME_FUNC},
        pith_name={PEP_CODE_PITH_ROOT_PARAM_NAME_PLACEHOLDER},
        pith_value={PEP_CODE_PITH_ROOT_NAME},
    )'''
'''
`PEP 484`_-compliant code snippet calling the decorated callable annotated by
the :attr:`typing.NoReturn` singleton and raising an exception if this call
successfully returned a value rather than raising an exception or halting the
active Python interpreter.

.. _PEP 484:
   https://www.python.org/dev/peps/pep-0484
'''

# ....................{ HINT ~ placeholder : child        }....................
PEP_CODE_HINT_CHILD_PLACEHOLDER_PREFIX = '@['
'''
Prefix of each **placeholder hint child type-checking substring** (i.e.,
placeholder to be globally replaced by a Python code snippet type-checking the
current pith expression against the currently iterated child hint of the
currently visited parent hint).
'''


PEP_CODE_HINT_CHILD_PLACEHOLDER_SUFFIX = ')!'
'''
Suffix of each **placeholder hint child type-checking substring** (i.e.,
placeholder to be globally replaced by a Python code snippet type-checking the
current pith expression against the currently iterated child hint of the
currently visited parent hint).
'''

# ....................{ HINT ~ placeholder : forwardref   }....................
PEP_CODE_HINT_FORWARDREF_UNQUALIFIED_PLACEHOLDER_PREFIX = '${FORWARDREF:'
'''
Prefix of each **placeholder unqualified forward reference classname
substring** (i.e., placeholder to be globally replaced by a Python code snippet
evaluating to the currently visited unqualified forward reference hint
canonicalized into a fully-qualified classname relative to the external
caller-defined module declaring the currently decorated callable).
'''


PEP_CODE_HINT_FORWARDREF_UNQUALIFIED_PLACEHOLDER_SUFFIX = ']?'
'''
Suffix of each **placeholder unqualified forward reference classname
substring** (i.e., placeholder to be globally replaced by a Python code snippet
evaluating to the currently visited unqualified forward reference hint
canonicalized into a fully-qualified classname relative to the external
caller-defined module declaring the currently decorated callable).
'''

# ....................{ HINT ~ pith : root                }....................
PEP_CODE_CHECK_HINT_ROOT = f'''
        # Type-check this passed parameter or return value against this
        # PEP-compliant type hint.
        if not {{hint_child_placeholder}}:
            __beartype_raise_pep_call_exception(
                func={PARAM_NAME_FUNC},
                pith_name={PEP_CODE_PITH_ROOT_PARAM_NAME_PLACEHOLDER},
                pith_value={PEP_CODE_PITH_ROOT_NAME},
            )
'''
'''
PEP-compliant code snippet type-checking the **root pith** (i.e., value of the
current parameter or return value) against the root PEP-compliant type hint
annotating that pith.

Design
----------
**This string is the only code snippet defined by this submodule to raise an
exception.** All other such snippets only test the current pith against the
current child PEP-compliant type hint and are thus intended to be dynamically
embedded
'''

# ....................{ HINT ~ nonpep                     }....................
PEP_CODE_CHECK_HINT_NONPEP_TYPE = (
    '''isinstance({pith_curr_expr}, {hint_curr_expr})''')
'''
PEP-compliant code snippet type-checking the current pith against the
current child PEP-compliant type expected to be a trivial non-:mod:`typing`
type (e.g., :class:`int`, :class:`str`).
'''

# ....................{ HINT ~ sequence : standard        }....................
PEP_CODE_CHECK_HINT_SEQUENCE_STANDARD = '''(
{indent_curr}    # True only if this pith shallowly satisfies this hint.
{indent_curr}    isinstance({pith_curr_assign_expr}, {hint_curr_expr}) and
{indent_curr}    # True only if either this pith is empty *OR* this pith is
{indent_curr}    # both non-empty and deeply satisfies this hint.
{indent_curr}    (not {pith_curr_assigned_expr} or {hint_child_placeholder})
{indent_curr})'''
'''
PEP-compliant code snippet type-checking the current pith against a parent
**standard sequence type** (i.e., PEP-compliant type hint accepting exactly one
subscripted type hint unconditionally constraining *all* items of this pith,
which necessarily satisfies the :class:`collections.abc.Sequence` protocol with
guaranteed ``O(1)`` indexation across all sequence items).

Caveats
----------
**This snippet cannot contain ternary conditionals.** For unknown reasons
suggesting a critical defect in the current implementation of Python 3.8's
assignment expressions, this snippet raises :class:`UnboundLocalError`
exceptions resembling the following when this snippet contains one or more
ternary conditionals:

    UnboundLocalError: local variable '__beartype_pith_1' referenced before assignment

In particular, the initial draft of this snippet guarded against empty
sequences with a seemingly reasonable ternary conditional:

.. code-block:: python

   PEP_CODE_CHECK_HINT_SEQUENCE_STANDARD = \'\'\'(
   {indent_curr}    isinstance({pith_curr_assign_expr}, {hint_curr_expr}) and
   {indent_curr}    {hint_child_placeholder} if {pith_curr_assigned_expr} else True
   {indent_curr})\'\'\'

That should behave as expected, but doesn't, presumably due to obscure scoping
rules and a non-intuitive implementation of ternary conditionals in CPython.
Ergo, the current version of this snippet guards against empty sequences with
disjunctions and conjunctions (i.e., ``or`` and ``and`` operators) instead.
Happily, the current version is more efficient than the equivalent approach
based on ternary conditional (albeit slightly less intuitive).
'''


PEP_CODE_CHECK_HINT_SEQUENCE_STANDARD_PITH_CHILD_EXPR = (
    '''{pith_curr_assigned_expr}[__beartype_random_int % len({pith_curr_assigned_expr})]''')
'''
PEP-compliant Python expression yielding the value of a randomly indexed item
of the current pith (which, by definition, *must* be a standard sequence).
'''

# ....................{ HINT ~ sequence : tuple           }....................
PEP_CODE_CHECK_HINT_TUPLE_FIXED_PREFIX = '''(
{indent_curr}    # True only if this pith is a tuple.
{indent_curr}    isinstance({pith_curr_assign_expr}, {hint_curr_expr}) and'''
'''
PEP-compliant code snippet prefixing all code type-checking the current pith
against each subscripted child hint of an itemized :class:`typing.Tuple` type
of the form ``typing.Tuple[{typename1}, {typename2}, ..., {typenameN}]``.
'''


PEP_CODE_CHECK_HINT_TUPLE_FIXED_SUFFIX = '''
{indent_curr})'''
'''
PEP-compliant code snippet suffixing all code type-checking the current pith
against each subscripted child hint of an itemized :class:`typing.Tuple` type
of the form ``typing.Tuple[{typename1}, {typename2}, ..., {typenameN}]``.
'''


PEP_CODE_CHECK_HINT_TUPLE_FIXED_EMPTY = '''
{{indent_curr}}    # True only if this tuple is empty.
{{indent_curr}}    not {pith_curr_assigned_expr} and'''
'''
PEP-compliant code snippet prefixing all code type-checking the current pith
to be empty against an itemized :class:`typing.Tuple` type of the non-standard
form ``typing.Tuple[()]``.

See Also
----------
:data:`PEP_CODE_CHECK_HINT_TUPLE_FIXED_NONEMPTY_CHILD`
    Further details.
'''


PEP_CODE_CHECK_HINT_TUPLE_FIXED_LEN = '''
{{indent_curr}}    # True only if this tuple is of the expected length.
{{indent_curr}}    len({pith_curr_assigned_expr}) == {hint_childs_len} and'''
'''
PEP-compliant code snippet prefixing all code type-checking the current pith
to be of the expected length against an itemized :class:`typing.Tuple` type of
the non-standard form ``typing.Tuple[()]``.

See Also
----------
:data:`PEP_CODE_CHECK_HINT_TUPLE_FIXED_NONEMPTY_CHILD`
    Further details.
'''


PEP_CODE_CHECK_HINT_TUPLE_FIXED_NONEMPTY_CHILD = '''
{{indent_curr}}    # True only if this item of this non-empty tuple deeply
{{indent_curr}}    # satisfies this child hint.
{{indent_curr}}    {hint_child_placeholder} and'''
'''
PEP-compliant code snippet type-checking the current pith against the current
child hint subscripting an itemized :class:`typing.Tuple` type of the form
``typing.Tuple[{typename1}, {typename2}, ..., {typenameN}]``.

Caveats
----------
The caller is required to manually slice the trailing suffix ``" and"`` after
applying this snippet to the last subscripted child hint of an itemized
:class:`typing.Tuple` type. While there exist alternate and more readable means
of accomplishing this, this approach is the optimally efficient.

The ``{indent_curr}`` format variable is intentionally brace-protected to
efficiently defer its interpolation until the complete PEP-compliant code
snippet type-checking the current pith against *all* subscripted arguments of
this parent type has been generated.
'''


PEP_CODE_CHECK_HINT_TUPLE_FIXED_NONEMPTY_PITH_CHILD_EXPR = (
    '''{pith_curr_assigned_expr}[{pith_child_index}]''')
'''
PEP-compliant Python expression yielding the value of the currently indexed
item of the current pith (which, by definition, *must* be a tuple).
'''

# ....................{ HINT ~ pep484 : generic           }....................
PEP484_CODE_CHECK_HINT_GENERIC_PREFIX = '''(
{indent_curr}    # True only if this pith is an instance of this generic.
{indent_curr}    isinstance({pith_curr_assign_expr}, {hint_curr_expr}) and'''
'''
PEP-compliant code snippet prefixing all code type-checking the current pith
against each unerased pseudo-superclass subclassed by a `PEP 484`_-compliant
**generic** (i.e., PEP-compliant type hint subclassing a combination of one or
more of the :mod:`typing.Generic` superclass, the :mod:`typing.Protocol`
superclass, and/or other :mod:`typing` non-class objects).

Caveats
----------
The ``{indent_curr}`` format variable is intentionally brace-protected to
efficiently defer its interpolation until the complete PEP-compliant code
snippet type-checking the current pith against *all* subscripted arguments of
this parent type has been generated.

.. _PEP 484:
   https://www.python.org/dev/peps/pep-0484
'''


PEP484_CODE_CHECK_HINT_GENERIC_SUFFIX = '''
{indent_curr})'''
'''
PEP-compliant code snippet suffixing all code type-checking the current pith
against each unerased pseudo-superclass subclassed by a `PEP 484`_-compliant
generic.

.. _PEP 484:
   https://www.python.org/dev/peps/pep-0484
'''


PEP484_CODE_CHECK_HINT_GENERIC_CHILD = '''
{{indent_curr}}    # True only if this pith deeply satisfies this unerased
{{indent_curr}}    # pseudo-superclass of this generic.
{{indent_curr}}    {hint_child_placeholder} and'''
'''
PEP-compliant code snippet type-checking the current pith against the current
unerased pseudo-superclass subclassed by a `PEP 484`_-compliant generic.

Caveats
----------
The caller is required to manually slice the trailing suffix ``" and"`` after
applying this snippet to the last unerased pseudo-superclass of such a generic.
While there exist alternate and more readable means of accomplishing this, this
approach is the optimally efficient.

The ``{indent_curr}`` format variable is intentionally brace-protected to
efficiently defer its interpolation until the complete PEP-compliant code
snippet type-checking the current pith against *all* subscripted arguments of
this parent type has been generated.
'''

# ....................{ HINT ~ pep484 : union             }....................
PEP484_CODE_CHECK_HINT_UNION_PREFIX = '''('''
'''
PEP-compliant code snippet prefixing all code type-checking the current pith
against each subscripted argument of a :class:`typing.Union` type.
'''


PEP484_CODE_CHECK_HINT_UNION_SUFFIX = '''
{indent_curr})'''
'''
PEP-compliant code snippet suffixing all code type-checking the current pith
against each subscripted argument of a :class:`typing.Union` type.
'''


PEP484_CODE_CHECK_HINT_UNION_CHILD_PEP = '''
{{indent_curr}}    {hint_child_placeholder} or'''
'''
PEP-compliant code snippet type-checking the current pith against the current
PEP-compliant child argument subscripting a parent :class:`typing.Union` type.

Caveats
----------
The caller is required to manually slice the trailing suffix ``" or"`` after
applying this snippet to the last subscripted argument of a
:class:`typing.Union` type. While there exist alternate and more readable means
of accomplishing this, this approach is the optimally efficient.

The ``{indent_curr}`` format variable is intentionally brace-protected to
efficiently defer its interpolation until the complete PEP-compliant code
snippet type-checking the current pith against *all* subscripted arguments of
this parent type has been generated.
'''


PEP484_CODE_CHECK_HINT_UNION_CHILD_NONPEP = '''
{{indent_curr}}    isinstance({pith_curr_expr}, {hint_curr_expr}) or'''
'''
PEP-compliant code snippet type-checking the current pith against the current
PEP-noncompliant child argument subscripting a parent :class:`typing.Union`
type.

See Also
----------
:data:`PEP484_CODE_CHECK_HINT_UNION_CHILD_PEP`
    Further details.
'''

# ....................{ FORMATTERS                        }....................
# Bound format methods of string globals defined above, preserved as discrete
# global variables for efficient lookup elsewhere.

# Bound format methods of string globals imported above.
PEP_CODE_CHECK_HINT_NONPEP_TYPE_format = (
    PEP_CODE_CHECK_HINT_NONPEP_TYPE.format)
PEP484_CODE_CHECK_HINT_GENERIC_CHILD_format = (
    PEP484_CODE_CHECK_HINT_GENERIC_CHILD.format)
PEP_CODE_CHECK_HINT_SEQUENCE_STANDARD_format = (
    PEP_CODE_CHECK_HINT_SEQUENCE_STANDARD.format)
PEP_CODE_CHECK_HINT_SEQUENCE_STANDARD_PITH_CHILD_EXPR_format = (
    PEP_CODE_CHECK_HINT_SEQUENCE_STANDARD_PITH_CHILD_EXPR.format)
PEP_CODE_CHECK_HINT_TUPLE_FIXED_EMPTY_format = (
    PEP_CODE_CHECK_HINT_TUPLE_FIXED_EMPTY.format)
PEP_CODE_CHECK_HINT_TUPLE_FIXED_LEN_format = (
    PEP_CODE_CHECK_HINT_TUPLE_FIXED_LEN.format)
PEP_CODE_CHECK_HINT_TUPLE_FIXED_NONEMPTY_CHILD_format = (
    PEP_CODE_CHECK_HINT_TUPLE_FIXED_NONEMPTY_CHILD.format)
PEP_CODE_CHECK_HINT_TUPLE_FIXED_NONEMPTY_PITH_CHILD_EXPR_format = (
    PEP_CODE_CHECK_HINT_TUPLE_FIXED_NONEMPTY_PITH_CHILD_EXPR.format)
PEP484_CODE_CHECK_HINT_UNION_CHILD_PEP_format = (
    PEP484_CODE_CHECK_HINT_UNION_CHILD_PEP.format)
PEP484_CODE_CHECK_HINT_UNION_CHILD_NONPEP_format = (
    PEP484_CODE_CHECK_HINT_UNION_CHILD_NONPEP.format)
PEP_CODE_PITH_ASSIGN_EXPR_format = PEP_CODE_PITH_ASSIGN_EXPR.format
