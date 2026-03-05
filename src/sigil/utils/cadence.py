# ~/sigil/src/sigil/utils/cadence.py
from __future__ import annotations
import inspect, typing as t, asyncio as aio
from concurrent.futures import ThreadPoolExecutor as TPE

import typical as typ

from sigil.logs import log

class __synced:
    """Utilities for handling synchronous callables and converting async to sync."""

    def check(self, call: typ.Call) -> bool:
        """Check if callable is synchronous."""
        return not inspect.iscoroutinefunction(call)

    def wrap(self, call: typ.Async) -> typ.Sync:
        """Wrap async callable to be callable synchronously."""
        routine = lambda c: t.cast(t.Coroutine, c)

        def wrapper(*args, **kwargs):
            coro = call(*args, **kwargs)

            try:
                aio.get_running_loop()
            except RuntimeError:
                return aio.run(routine(coro))

            with TPE() as pool:
                future = pool.submit(aio.run, routine(coro))
                return future.result()

        return wrapper

    def eval(self, call: typ.Call, *args, **kwargs) -> t.Any:
        """Evaluate callable synchronously, wrapping if async."""
        if self.check(call):
            return call(*args, **kwargs)
        return self.wrap(call)(*args, **kwargs)

    @t.overload
    def __call__(self, call: typ.Call, eval: t.Literal[False] = ..., *args, **kwargs) -> typ.Sync: ...

    @t.overload
    def __call__(self, call: typ.Call, eval: t.Literal[True], *args, **kwargs) -> t.Any: ...

    def __call__(
        self,
        call: typ.Call,
        eval: bool = False,
        *args, **kwargs
        ) -> typ.Sync | t.Any:  # inline union instead of Synced
        """
        Get sync version of callable or evaluate it.

        Args:
            call: Callable to process
            eval: If True, evaluate immediately; if False, return wrapped callable
        """
        match ((not self.check(call)), eval):
            case (False, False): return call
            case (True, False): return self.wrap(call)
            case _: return self.eval(call, *args, **kwargs)

    ## stubbed for later ##
    def batch(self, *calls: typ.Call, **kwargs) -> list[t.Any]:
        """Execute multiple callables synchronously, wrapping async ones."""
        raise NotImplementedError

    def timeout(self, call: typ.Call, seconds: float, *args, **kwargs) -> t.Any:
        """Execute callable with timeout."""
        raise NotImplementedError

    def retry(self, call: typ.Call, attempts: int = 3, *args, **kwargs) -> t.Any:
        """Execute callable with retry logic."""
        raise NotImplementedError

    def map(self, call: typ.Call, iterable: t.Iterable, **kwargs) -> list[t.Any]:
        """Map callable over iterable synchronously."""
        raise NotImplementedError

synced = __synced()

class __asynced:
    """Utilities for handling async callables and converting sync to async."""

    def check(self, call: typ.Call) -> bool:
        """Check if callable is asynchronous."""
        return inspect.iscoroutinefunction(call)

    def wrap(self, call: typ.Sync) -> typ.Async:
        """Wrap sync callable to be awaitable."""
        async def wrapper(*args, **kwargs):
            return await aio.to_thread(call, *args, **kwargs)
        return wrapper

    async def eval(self, call: typ.Call, *args, **kwargs) -> t.Any:
        """Evaluate callable asynchronously, wrapping if sync."""
        if self.check(call):
            return await call(*args, **kwargs)
        return await self.wrap(call)(*args, **kwargs)

    def __call__(self, call: typ.Call) -> typ.Async:
        """Get async version of callable."""
        if self.check(call):
            return call
        return self.wrap(call)

    ## stubbed for later ##
    async def gather(self, *calls: typ.Call, **kwargs) -> list[t.Any]:
        """Gather multiple callables as async tasks."""
        raise NotImplementedError

    async def timeout(self, call: typ.Call, seconds: float, *args, **kwargs) -> t.Any:
        """Execute callable with timeout."""
        raise NotImplementedError

    async def retry(self, call: typ.Call, attempts: int = 3, *args, **kwargs) -> t.Any:
        """Execute callable with retry logic."""
        raise NotImplementedError

    async def map(self, call: typ.Call, iterable: t.Iterable, **kwargs) -> list[t.Any]:
        """Map callable over iterable asynchronously."""
        raise NotImplementedError

asynced = __asynced()
