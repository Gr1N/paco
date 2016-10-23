# -*- coding: utf-8 -*-
import asyncio
from .decorator import decorate
from .assertions import assert_corofunction

ExceptionMessage = 'coroutine cannot be executed more than {} times'


@decorate
def times(coro, limit=1, raise_exception=False, return_value=None):
    """
    Creates a continuation coroutine function with some arguments
    already applied.

    Useful as a shorthand when combined with other control flow functions.
    Any arguments passed to the returned function are added to the arguments
    originally passed to apply.

    This is similar to partial.

    arguments:
        coro (coroutinefunction): coroutine function to wrap.
        limit (int): max limit of coroutine executions.
        raise_exception (bool): raise exception if execution times exceeded.
        return_value (mixed): value to return when execution times exceeded.

    Raises:
        TypeError: if coro argument is not a coroutine function.
        RuntimeError: if max execution excedeed (optional).

    Returns:
        coroutinefunction

    Usage::

        coro = pyco.times(coro, 3)
        coro(1)
        coro(2)
        coro(3)
        coro(4)  # ignored
    """
    assert_corofunction(coro=coro)

    # Store call times
    limit = max(limit, 1)
    times = limit

    # Store result from last execution
    result = None

    @asyncio.coroutine
    def wrapper(*args, **kw):
        nonlocal limit
        nonlocal result

        # Check execution limit
        if limit == 0:
            if raise_exception:
                raise RuntimeError(ExceptionMessage.format(times))
            if return_value:
                return return_value
            return result

        # Decreases counter
        limit -= 1

        # If return_value is present, do not memoize result
        if return_value:
            return (yield from coro(*args, **kw))

        # Schedule coroutine and memoize result
        result = yield from coro(*args, **kw)
        return result

    return wrapper
