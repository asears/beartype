#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2023 Beartype authors.
# See "LICENSE" for further details.

'''
:mod:`beartype.cave`-specific **abstract base classes (ABCs).**
'''

# ....................{ TODO                               }....................
#FIXME: Refactor this private submodule into a new public "beartype.caver"
#submodule, so-named as it enables users to externally create new ad-hoc
#protocols implementing structural subtyping resembling those predefined by
#"beartype.cave". To do so:
#
#* In the "beartype.caver" submodule:
#  * Define a new make_type_structural() function with signature resembling:
#    def make_type_structural(name: str, method_names: Iterable) -> type:
#  * Implement this function to dynamically create a new type with the passed
#    classname defining:
#    * Abstract methods with the passed method names.
#    * A __subclasshook__() dunder method checking the passed class for
#      concrete methods with these names.
#    To do so, note that abstract methods *CANNOT* be dynamically
#    monkey-patched in after class creation but *MUST* instead be statically
#    defined at class creation time (due to metaclass shenanigans).
#    Fortunately, doing so is trivial; simply use the three-argument form of
#    the type() constructor, as demonstrated by this StackOverflow answer:
#    https://stackoverflow.com/a/14219244/2809027
#  * *WAIT!* There's no need to call the type() constructor directly. Instead,
#    define a new make_type() function in this new submodule copied from the
#    betse.util.type.classes.define_class() function (but renamed, obviously).
#* Replace the current manual definition of "_BoolType" below with an in-place
#  call to that method from the "beartype.cave" submodule: e.g.,
#    BoolType = _make_type_structural(
#        name='BoolType', method_names=('__bool__',))
#
#Dis goin' be good.
#FIXME: Actually, don't do any of the above. That would simply be reinventing
#the wheel, as the "typing.Protocol" superclass already exists and is more than
#up to the task. In fact, once we drop support for Python < 3.7, we should:
#* Redefine the "_BoolType" class declared below should in terms of the
#  "typing.Protocol" superclass.
#* Shift the "_BoolType" class directly into the "beartype.cave" submodule.
#* Refactor away this entire submodule.

# ....................{ IMPORTS                            }....................
from abc import ABCMeta, abstractmethod

# ....................{ FUNCTIONS                          }....................
def _check_methods(C: type, *methods: str):
    '''
    Private utility function called by abstract base classes (ABCs) implementing
    structural subtyping by detecting whether the passed class or some
    superclass of that class defines all of the methods with the passed method
    names.

    For safety, this function has been duplicated as is from its eponymous
    counterpart in the private stdlib :mod:`_colletions_abc` module.

    Parameters
    ----------
    C : type
        Class to be validated as defining these methods.
    methods : Tuple[str, ...]
        Tuple of the names of all methods to validate this class as defining.

    Returns
    ----------
    Either:

        * ``True`` if this class defines all of these methods.
        * ``NotImplemented`` if this class fails to define one or more of these
          methods.
    '''

    mro = C.__mro__
    for method in methods:
        for B in mro:  # pyright: ignore[reportGeneralTypeIssues]
            if method in B.__dict__:
                if B.__dict__[method] is None:
                    return NotImplemented
                break
        else:
            return NotImplemented

    return True

# ....................{ SUPERCLASSES                       }....................
class BoolType(object, metaclass=ABCMeta):
    '''
    TLDR
    ----
    Sometimes you want to know if something is true or false.
    
    For example, you might want to check if your answer is correct, or if you have enough money to buy a candy.
    In Python, you can use things called booleans to do that.
    
    Booleans are things that can be either True or False, like 1 + 1 == 2 or 3 > 4.

    But not everything in Python is a boolean.
    Some things are numbers, or words, or lists, or other kinds of stuff.
    
    How can you tell if something is a boolean or not?
    You can use a special function called isinstance that takes two things and tells you if the first thing
    is the same kind of stuff as the second thing.
    
    For example, isinstance(True, bool) will tell you that True is a boolean, but isinstance(42, bool) will tell you that 42 is not a boolean.

    But what if you want to use booleans from other programs that are not Python?
    For example, there is a program called NumPy that lets you do math with lots of numbers at once.
    
    NumPy has its own kind of booleans that are different from Python's booleans.
    They look like this: numpy.bool_(True).
    
    How can you use isinstance to check if something is a NumPy boolean?
    The answer is: you can't. isinstance(numpy.bool_(True), bool) will tell you that numpy.bool_(True)
    is not a boolean, even though it acts like one.
    That's because NumPy booleans are not made from the same stuff as Python booleans.
    
    They are made from different stuff that is faster for math, but not compatible with Python.
    So, how can you check if something is a boolean, no matter what kind of stuff it is made from?
    You can use a special thing from this part of the program called BooleanType.
    BooleanType is like a super-boolean that can match any kind of boolean, whether it is from Python or NumPy or somewhere else.
    You can use isinstance with BooleanType to check if something is a boolean.
    
    For example, isinstance(numpy.bool_(True), BooleanType) will tell you that numpy.bool_(True) is a boolean.

    But how does BooleanType work? How can it match any kind of boolean? Well, it uses a trick called structural subtyping.
    That means it looks at what a thing can do, not what it is made from.
    
    If a thing can do something that a boolean can do, then it is a boolean.
    For example, a boolean can do this: bool(True).
    If a thing can do that, then it is a boolean.
    BooleanType checks if a thing can do that, and if it can, then it says that it is a boolean.

    But why do we need BooleanType? Why can't we just use bool to check if something is a boolean?
    Well, because bool does more than just check. It also changes things. For example, bool(0) will change 0 into False.
    Sometimes you don't want to change things, you just want to check them. That's when you use BooleanType.

    So, BooleanType is a cool thing that lets you check if something is a boolean,
    no matter what kind of stuff it is made from. It uses a trick called structural subtyping to look at what a thing can do,
    not what it is made from. It is faster and simpler than typing, which is another part of the program that lets you check more things,
    but also makes your program slower and more complicated.
    
    BooleanType is not part of the official rules of Python, but some people like to use it anyway.
    ----

    Type of all **booleans** (i.e., objects defining the ``__bool__()`` dunder
    method; objects reducible in boolean contexts like ``if`` conditionals to
    either ``True`` or ``False``).

    This type matches:

    * **Builtin booleans** (i.e., instances of the standard :class:`bool` class
      implemented in low-level C).
    * **NumPy booleans** (i.e., instances of the :class:`numpy.bool_` class
      implemented in low-level C and Fortran) if :mod:`numpy` is importable.

    Usage
    ----------
    Non-standard boolean types like NumPy booleans are typically *not*
    interoperable with the standard standard :class:`bool` type. In particular,
    it is typically *not* the case, for any variable ``my_bool`` of
    non-standard boolean type and truthy value, that either ``my_bool is True``
    or ``my_bool == True`` yield the desired results. Rather, such variables
    should *always* be coerced into the standard :class:`bool` type before
    being compared -- either:

    * Implicitly (e.g., ``if my_bool: pass``).
    * Explicitly (e.g., ``if bool(my_bool): pass``).

    Caveats
    ----------
    **There exists no abstract base class governing booleans in Python.**
    Although various Python Enhancement Proposals (PEPs) were authored on the
    subject, all were rejected as of this writing. Instead, this type trivially
    implements an ad-hoc abstract base class (ABC) detecting objects satisfying
    the boolean protocol via structural subtyping. Although no actual
    real-world classes subclass this :mod:`beartype`-specific ABC, the
    detection implemented by this ABC suffices to match *all* boolean types.

    See Also
    ----------
    :class:`beartype.cave.ContainerType`
        Further details on structural subtyping.
    '''

    # ..................{ DUNDERS                            }..................
    # This abstract base class (ABC) has been implemented ala standard
    # container ABCs in the private stdlib "_collections_abc" module (e.g., the
    # trivial "_collections_abc.Sized" type).
    __slots__ = ()

    @abstractmethod
    def __bool__(self):
        return False

    @classmethod
    def __subclasshook__(cls, C):
        if cls is BoolType:
            return _check_methods(C, '__bool__')
        return NotImplemented
