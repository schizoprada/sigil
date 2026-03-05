# ~/sigil/src/sigil/sym/core/base.py
"""
Base classes for predicates and propositions.

Provides composable predicate primitives with operator overloading
for logical composition.
"""
from __future__ import annotations
import typing as t

import typical as typ

from sigil.logs import log
from sigil.utils import synced

class Predicate:
    """Wraps any predicate callable to make it composable."""

    @t.runtime_checkable
    class Protocol(t.Protocol):
        def __call__(self, *args, **kwargs) -> bool: ...

    def __init__(self, fn: typ.Predicate | Predicate) -> None:
        self.fn = fn.fn if isinstance(fn, Predicate) else fn

    def __call__(self, *args, **kwargs) -> bool:
        return synced.eval(self.fn, *args, **kwargs)

    @classmethod
    def wrap(cls, fn: typ.Predicate | Predicate) -> Predicate:
        """Wrap a callable as a Predicate if not already wrapped."""
        if isinstance(fn, Predicate): return fn
        return cls(fn)

    def __and__(self, other: typ.Predicate | Predicate) -> Predicate:
        """Compose with AND logic."""
        return And(self, self.wrap(other))

    def __or__(self, other: typ.Predicate | Predicate) -> Predicate:
        """Compose with OR logic."""
        return Or(self, self.wrap(other))

    def __invert__(self) -> Predicate:
        """Negate the predicate."""
        return Not(self)


class And(Predicate):
    """Composed predicate using AND logic."""

    def __init__(self, left: Predicate, right: Predicate):
        self.left = left
        self.right = right

    def __call__(self, *args, **kwargs) -> bool:
        return self.left(*args, **kwargs) and self.right(*args, **kwargs)


class Or(Predicate):
    """Composed predicate using OR logic."""

    def __init__(self, left: Predicate, right: Predicate):
        self.left = left
        self.right = right

    def __call__(self, *args, **kwargs) -> bool:
        return self.left(*args, **kwargs) or self.right(*args, **kwargs)


class Not(Predicate):
    """Negated predicate."""

    def __init__(self, pred: Predicate):
        self.pred = pred

    def __call__(self, *args, **kwargs) -> bool:
        return not self.pred(*args, **kwargs)


def predicate(fn: typ.Predicate) -> Predicate:
    """Wrap a callable as a composable Predicate."""
    return Predicate(fn)
