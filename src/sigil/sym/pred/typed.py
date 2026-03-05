# ~/sigil/src/sigil/sym/pred/typed.py
"""
Type-based predicates.

Predicates for type checking and validation.
"""
from __future__ import annotations
import typing as t

import typical as typ

from sigil.logs import log
from sigil.sym.core.base import Predicate


class Instance(Predicate):
    """Check if value is instance of type(s)."""

    def __init__(self, *types: type):
        self.types = types

    def __call__(self, value: t.Any) -> bool:
        return isinstance(value, self.types)


class Subclass(Predicate):
    """Check if value is subclass of type(s)."""

    def __init__(self, *types: type):
        self.types = types

    def __call__(self, value: type) -> bool:
        return issubclass(value, self.types)


class OfType(Predicate):
    """Check if type(value) matches target type exactly."""

    def __init__(self, target: type):
        self.target = target

    def __call__(self, value: t.Any) -> bool:
        return type(value) is self.target


# Factory functions
def instance(*types: type) -> Instance:
    """Create predicate for isinstance check."""
    return Instance(*types)


def subclass(*types: type) -> Subclass:
    """Create predicate for issubclass check."""
    return Subclass(*types)


def oftype(target: type) -> OfType:
    """Create predicate for exact type match."""
    return OfType(target)
