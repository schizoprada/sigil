# ~/sigil/src/sigil/sym/pred/prim.py
"""
Primitive predicate implementations.

Basic predicates for common checking operations that aren't easily
expressible via builtins or would require verbose lambdas.
"""
from __future__ import annotations
import typing as t

import typical as typ

from sigil.logs import log
from sigil.sym.core.base import Predicate


class NotNone(Predicate):
    """Check if value is not None."""

    def __init__(self):
        pass

    def __call__(self, value: t.Any) -> bool:
        return value is not None


class Truthy(Predicate):
    """Check if value is truthy."""

    def __init__(self):
        pass

    def __call__(self, value: t.Any) -> bool:
        return bool(value)

class Falsy(Predicate):
    """Check if value is falsy."""

    def __init__(self):
        pass

    def __call__(self, value: t.Any) -> bool:
        return not bool(value)

class IsEmpty(Predicate):
    """Check if collection is empty."""

    def __init__(self):
        pass

    def __call__(self, value: t.Any) -> bool:
        return len(value) == 0

class NotEmpty(Predicate):
    """Check if collection is not empty."""

    def __init__(self):
        pass

    def __call__(self, value: t.Any) -> bool:
        return len(value) > 0

class Always(Predicate):
    """Always returns True."""

    def __init__(self):
        pass

    def __call__(self, *args, **kwargs) -> bool:
        return True


class Never(Predicate):
    """Always returns False."""

    def __init__(self):
        pass

    def __call__(self, *args, **kwargs) -> bool:
        return False

class Inside(Predicate):
    """Check if value is inside container."""

    def __init__(self, container: t.Any):
        self.container = container

    def __call__(self, value: t.Any) -> bool:
        return value in self.container


class Has(Predicate):
    """Check if object has attribute."""

    def __init__(self, attr: str):
        self.attr = attr

    def __call__(self, obj: t.Any) -> bool:
        return hasattr(obj, self.attr)

# Singleton instances
notnone = NotNone()
truthy = Truthy()
falsy = Falsy()
isempty = IsEmpty()
notempty = NotEmpty()
always = Always()
never = Never()

# Factory functions for parameterized predicates
def inside(container: t.Any) -> Inside:
    """Create predicate to check if value is in container."""
    return Inside(container)


def has(attr: str) -> Has:
    """Create predicate to check if object has attribute."""
    return Has(attr)
