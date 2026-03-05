# ~/sigil/src/sigil/route/base.py
"""
Function routing and dispatching utilities.

Register multiple handlers and route calls based on predicates.
"""
from __future__ import annotations
import typing as t

import typical as typ

from sigil.logs import log
from sigil.sym import predicate as __predicate, Predicate
from sigil.utils import synced, asynced

class Router:
    """Generic dispatcher - register handlers with predicates."""

    def __init__(self, autoawait: bool = True) -> None:
        self.autoawait = autoawait
        self.registry: list[tuple[typ.Call, list[Predicate]]] = []

    def __decorating(self, *args) -> bool:
        return (
            bool(args)
            and callable(args[0])
            and all(
                (
                    isinstance(a, Predicate)
                    or typ.ispredicate(a, strict=True)
                )
                for a in args
            )
        )

    def register(self, *predicates: Predicate | typ.Predicate) -> typ.Decorator:
        def decorator(fn: typ.Call) -> typ.Call:
            self.registry.append((fn, list(map(__predicate, predicates)))) # should make more efficient
            return fn
        return decorator

    def __call__(self, *args, **kwargs):
        if self.__decorating(*args):
            return self.register(*args)

        for fn, preds in self.registry:
            if all(p(*args, **kwargs) for p in preds):
                if asynced.check(fn):
                    if self.autoawait:
                        return synced.eval(fn, *args, **kwargs)
                return fn(*args, **kwargs)
        raise ValueError(f"[{self.__class__.__name__}] no function available for provided:\n{args}\n{kwargs}")
