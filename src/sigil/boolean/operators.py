# ~/sigil/src/sigil/boolean/operators.py
from __future__ import annotations
import typing as t


class __unary:
    def negation(self, a: bool) -> bool: return (not a)
unary = __unary()

class __binary:
    def conjunction(self, a: bool, b: bool) -> bool: return (a and b)
    def disjunction(self, a: bool, b: bool) -> bool: return (a or b)
    def xor(self, a: bool, b: bool) -> bool: return (a is not b)
    def xnor(self, a: bool, b: bool) -> bool: return (a is b)
    def nor(self, a: bool, b: bool) -> bool: return (not (a or b))
    def nand(self, a: bool, b: bool) -> bool: return (not (a and b))
