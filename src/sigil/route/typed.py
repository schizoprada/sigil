# ~/sigil/src/sigil/route/typed.py
"""
"""
from __future__ import annotations
import typing as t

import typical as typ

from sigil.logs import log
from sigil.sym import Predicate, predicate as predwrap
from sigil.route.base import Router





class TypeRouter(Router):
    """
    Route calls based on argument types.

    Usage:
        handle = TypeRouter()

        # Explicit types
        @handle(int, str)
        def fn1(x: int, y: str): ...

        # Implicit from signature
        @handle
        def fn2(x: float): ...

        handle(1, "hello")  # routes to fn1
        handle(3.14)  # routes to fn2
    """
