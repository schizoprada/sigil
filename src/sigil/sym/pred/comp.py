# ~/sigil/src/sigil/sym/pred/comp.py
"""
Comparison predicates.

Predicates for comparing values, positions, and relationships.
"""
from __future__ import annotations
import typing as t, operator as op

import typical as typ

from sigil.logs import log
from sigil.sym.core.base import Predicate


class Equal(Predicate):
    """Check if value equals target."""

    def __init__(self, target: t.Any):
        self.target = target

    def __call__(self, value: t.Any) -> bool:
        return op.eq(value, self.target)


class NotEqual(Predicate):
    """Check if value does not equal target."""

    def __init__(self, target: t.Any):
        self.target = target

    def __call__(self, value: t.Any) -> bool:
        return op.ne(value, self.target)


class Greater(Predicate):
    """Check if value is greater than target."""

    def __init__(self, target: t.Any):
        self.target = target

    def __call__(self, value: t.Any) -> bool:
        return op.gt(value, self.target)


class Less(Predicate):
    """Check if value is less than target."""

    def __init__(self, target: t.Any):
        self.target = target

    def __call__(self, value: t.Any) -> bool:
        return op.lt(value, self.target)


class GreaterEqual(Predicate):
    """Check if value is greater than or equal to target."""

    def __init__(self, target: t.Any):
        self.target = target

    def __call__(self, value: t.Any) -> bool:
        return op.ge(value, self.target)


class LessEqual(Predicate):
    """Check if value is less than or equal to target."""

    def __init__(self, target: t.Any):
        self.target = target

    def __call__(self, value: t.Any) -> bool:
        return op.le(value, self.target)


class Between(Predicate):
    """Check if value is between low and high (inclusive)."""

    def __init__(self, low: t.Any, high: t.Any):
        self.low = low
        self.high = high

    def __call__(self, value: t.Any) -> bool:
        return self.low <= value <= self.high


class Index(Predicate):
    """Check if positional index matches target."""

    def __init__(self, target: int):
        self.target = target

    def __call__(self, idx: int) -> bool:
        return idx == self.target


# Factory functions
def equal(target: t.Any) -> Equal:
    """Create predicate for equality check."""
    return Equal(target)


def notequal(target: t.Any) -> NotEqual:
    """Create predicate for inequality check."""
    return NotEqual(target)


def greater(target: t.Any) -> Greater:
    """Create predicate for greater-than check."""
    return Greater(target)


def less(target: t.Any) -> Less:
    """Create predicate for less-than check."""
    return Less(target)


def greaterequal(target: t.Any) -> GreaterEqual:
    """Create predicate for greater-or-equal check."""
    return GreaterEqual(target)


def lessequal(target: t.Any) -> LessEqual:
    """Create predicate for less-or-equal check."""
    return LessEqual(target)


def between(low: t.Any, high: t.Any) -> Between:
    """Create predicate for between check."""
    return Between(low, high)


def index(target: int) -> Index:
    """Create predicate for index matching."""
    return Index(target)


# shorthands #
eq = equal
neq = notequal
gt = greater
lt = less
gte = greaterequal
lte = lessequal
btw = between
idx = index
