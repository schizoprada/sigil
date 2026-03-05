"""
sigil
"""
__author__ = "Joel Yisrael"
__version__ = "0.0.0"

VERSION = tuple(map(int, __version__.split('.')))

from .utils import (
    synced, asynced
)
from .sym import (
    Predicate, And, Or, Not,
    predicate,
    notnone, truthy, falsy,
    isempty, notempty, always,
    never, inside, has,
    equal, notequal,
    greater, less,
    greaterequal,
    lessequal,
    between, index,
    eq, neq, gt, lt,
    gte, lte, btw, idx,
    instance, subclass, oftype
)
from .fnx import(
    sift, satisfies, resolve
)
