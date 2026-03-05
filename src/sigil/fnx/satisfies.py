# ~/sigil/src/sigil/fnx/satisfies.py
"""
Signature satisfaction checking utilities.

Validate if provided arguments satisfy a callable's signature requirements.
"""
from __future__ import annotations
import inspect, typing as t

import typical as typ
from sigil.logs import log
from sigil.sym import Predicate

class matches:
    @staticmethod
    def types(idx: int, param: inspect.Parameter, args: tuple, kwargs: dict) -> bool:
        if (param.annotation == inspect.Parameter.empty): return True
        pos = (idx < len(args))
        key = (param.name in kwargs)
        if not (pos or key): return True
        if (pos and key): return False
        value = args[idx] if pos else kwargs[param.name]

        try: return isinstance(value, param.annotation)
        except TypeError: return True # Can't check complex types

        raise

    @staticmethod
    def required(idx: int, param: inspect.Parameter, args: tuple, kwargs: dict) -> bool:
        pos = (idx < len(args))
        key = (param.name in kwargs)
        opt = (param.default != inspect.Parameter.empty) # is optional // has default
        if (pos and key): return False
        if (param.kind == inspect.Parameter.POSITIONAL_ONLY):
            if key: return False # Violation: pos-only provided as kwarg
            if not opt: return pos
            return True # has default

        if (param.kind == inspect.Parameter.KEYWORD_ONLY):
            if not opt: return key
            return True

        # Positional or keyword - can be either
        # If required, must be provided somehow
        if not opt: return (pos or key)

        # Has default - optional, always satisfied
        return True


class __satisfies:
    """Check if args/kwargs satisfy a callable's signature."""

    def check(
        self,
        fn: typ.Call,
        *args,
        predicate: typ.Predicate | Predicate,
        **kwargs
        ) -> bool:
        skip = lambda p: (p.kind in [inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD])
        params = list(inspect.signature(fn).parameters.values())

        return all(
            predicate(i, p, args, kwargs)
            for i, p in enumerate(params)
            if not skip(p)
        )

    def __call__(
        self,
        fn: typ.Call,
        *args,
        types: bool = True,
        required: bool = True,
        **kwargs
        ) -> bool:
        if not (types or required): return True
        if types:
            if not self.check(
                fn, *args, predicate=matches.types, **kwargs
            ):
                return False
        if required:
            if not self.check(
                fn, *args, predicate=matches.required, **kwargs
            ):
                return False
        return True

satisfies = __satisfies()
