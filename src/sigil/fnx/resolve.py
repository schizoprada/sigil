# ~/sigil/src/sigil/fnx/resolve.py
from __future__ import annotations
import typing as t, functools as ft

import typical as typ
from sigil.logs import log
from sigil.fnx.sift import sift
from sigil.fnx.satisfies import satisfies

class __resolve:
    """Resolve and bind arguments to callables."""
    def bind(
        self,
        fn: typ.Call,
        *args,
        sifter: typ.Sync = sift.__call__,
        validator: t.Optional[typ.Sync] = satisfies.__call__,
        **kwargs
        ) -> typ.Call:
        if (validator is not None):
            if not validator(fn, *args, **kwargs):
                raise ValueError(f"...")
        a, kw = sifter(fn, *args, **kwargs)
        return ft.partial(fn, *a, **kw)

    def __call__(
        self,
        fn: typ.Call,
        *args,
        sifter: typ.Sync = sift.__call__,
        validator: t.Optional[typ.Sync] = satisfies.__call__,
        **kwargs
        ) -> typ.Call: return self.bind(
            fn, *args, sifter=sifter,
            validator=validator, **kwargs
        )

    ## todo:
        # context manager

resolve = __resolve()
