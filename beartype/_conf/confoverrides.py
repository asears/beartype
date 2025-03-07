#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2023 Beartype authors.
# See "LICENSE" for further details.

'''
Beartype **hint overrides class hierarchy** (i.e., public classes implementing
immutable mappings intended to be passed as the value of the ``hint_overrides``
parameter accepted by the :class:`beartype.BeartypeConf.__init__` method).
'''

# ....................{ IMPORTS                            }....................
from beartype.roar import BeartypeHintOverridesException
from beartype._util.kind.map.utilmapfrozen import FrozenDict
from re import (
    escape as re_escape,
    search as re_search,
)

# ....................{ CLASSES                            }....................
#FIXME: Unit test us up, please.
class BeartypeHintOverrides(FrozenDict):
    '''
    Beartype **hint overrides** (i.e., immutable mapping intended to be passed
    as the value of the ``hint_overrides`` parameter accepted by the
    :class:`beartype.BeartypeConf.__init__` method).
    '''

    # ..................{ INITIALIZERS                       }..................
    def __init__(self, *args, **kwargs) -> None:

        # Instantiate this immutable dictionary with all passed parameters.
        super().__init__(*args, **kwargs)

        # For each source and target hint override in this dictionary...
        for hint_override_src, hint_override_trg in self.items():
            # The machine-readable representation of this source override,
            # escaped to protect all regex-specific syntax in this
            # representation from being erroneously parsed as that syntax.
            HINT_OVERRIDE_SRC_REPR = re_escape(repr(hint_override_src))

            # Regular expression matching subscription-style recursion in this
            # hint override (e.g., 'str: list[str]').
            #
            # Note that:
            # * Beartype currently only supports union-style recursion (e.g.,
            #   "float: int | float").
            # * Regular expressions inevitably fail in edge cases (e.g.,
            #   "str: Literal['str']"). Thankfully, hint overrides *AND* these
            #   edge cases are sufficiently rare that we can conveniently ignore
            #   them until some GitHub pyromaniac inevitably complains and
            #   starts lighting dumpster fires on our issue tracker.
            HINT_OVERRIDE_RECURSION_REGEX = (
                # An opening "[" delimeter followed by zero or more characters
                # that are *NOT* the corresponding closing "]" delimiter.
                r'\[[^]]*'
                # The machine-readable representation of this source override,
                # bounded on both sides by word boundaries.
                fr'\b{HINT_OVERRIDE_SRC_REPR}\b'
                # Zero or more characters that are *NOT* the corresponding
                # closing "]" delimiter followed by that delimiter.
                r'[^]]*\]'
            )

            # Match object if this hint override contains one or more instances
            # of subscription-style recursion *OR* "None" otherwise.
            hint_override_recursion = re_search(
                HINT_OVERRIDE_RECURSION_REGEX, repr(hint_override_trg))

            # If this hint override contains one or more instances of
            # subscription-style recursion, raise an exception.
            if hint_override_recursion is not None:
                raise BeartypeHintOverridesException(
                    f'Recursive type hint override '
                    f'{repr(hint_override_src)}: {repr(hint_override_trg)} '
                    f'currently unsupported. Please complain loudly on the '
                    f'@beartype issue tracker if you feel that this is dumb.'
                )
            # Else, this hint override contains *NO* such recursion.

# ....................{ GLOBALS                            }....................
BEARTYPE_HINT_OVERRIDES_EMPTY = BeartypeHintOverrides()
'''
**Empty frozen dictionary singleton** (i.e., :class:`.BeartypeHintOverrides`
instance containing *no* key-value pairs).
'''
