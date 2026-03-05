# ~/sigil/src/sigil/fnx/sift.py
"""
Parameter sifting and resolution utilities.

Extract and match arguments to callable signatures for parameter routing.
"""
from __future__ import annotations
import inspect, typing as t
from itertools import zip_longest as ziplong

import typical as typ
from sigil.logs import log
from sigil.sym import Predicate, index, instance

_MISSING = object()

def argmatch(arg: t.Any, param: inspect.Parameter) -> bool:
    """Default positional arg matching: type check."""
    # Position is already matched by loop structure
    # Just check if arg matches param type
    if param.annotation != inspect.Parameter.empty:
        try:
            return isinstance(arg, param.annotation)
        except TypeError:
            # Can't isinstance check complex types, skip type check
            pass
    return True

def kwargmatch(
    name: str,
    value: t.Any,
    param: inspect.Parameter
    ) -> bool:
    """Default kwarg matching: name match with optional type check."""
    if name != param.name:
        return False
    # Check type if annotated
    if param.annotation != inspect.Parameter.empty:
        try:
            return isinstance(value, param.annotation)
        except TypeError:
            pass
    return True

class __sift:
    """
    Sift arguments to match callable signatures.

    Provides flexible parameter extraction with customizable matching logic.
    """

    def positional(
        self,
        fn: typ.Call,
        *args,
        predicate: typ.Predicate | Predicate = argmatch,
        **kwargs
        ) -> list:
        params = list(inspect.signature(fn).parameters.values())
        result = []
        for param, arg in ziplong(params, args, fillvalue=_MISSING):
            if (arg is not _MISSING) and (param is not _MISSING):
                value = kwargs[param.name] if param.name in kwargs else arg # type: ignore
                if predicate(value, param):
                    result.append(value)
        return result

    def keyworded(
        self,
        fn: typ.Call,
        *args,
        predicate: typ.Predicate | Predicate = kwargmatch,
        **kwargs
        ) -> dict:
        sig = inspect.signature(fn)
        params = list(sig.parameters.values())
        result = {
            name: value for name, value
            in kwargs.items() if name in sig.parameters
            and predicate(name, value, sig.parameters[name])
        }
        # Convert positional args to kwargs using zip
        for param, arg in zip(params, args):
            if argmatch(arg, param):
                result[param.name] = arg

        return result

    def pos(
        self,
        fn: typ.Call,
        *args,
        predicate: typ.Predicate | Predicate = argmatch,
        **kwargs
        ) -> list: return self.positional(fn, *args, predicate, **kwargs)

    def kw(
        self,
        fn: typ.Call,
        *args,
        predicate: typ.Predicate | Predicate = kwargmatch,
        **kwargs
        ) -> dict: return self.keyworded(fn, *args, predicate, **kwargs)


    def __call__(
        self,
        fn: typ.Call,
        *args,
        returns: type = tuple,
        apred: typ.Predicate | Predicate = argmatch,
        kwpred: typ.Predicate | Predicate = kwargmatch,
        **kwargs
        ) -> list | dict | tuple[list, dict]:
        if returns is list: return self.positional(fn, *args, predicate=apred, **kwargs)
        if returns is dict: return self.keyworded(fn, *args, predicate=kwpred, **kwargs)
        return (
            self.positional(fn, *args, predicate=apred, **kwargs),
            self.keyworded(fn, *args, predicate=kwpred, **kwargs)
        )

sift = __sift()
