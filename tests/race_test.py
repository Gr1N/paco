# -*- coding: utf-8 -*-
import asyncio
from pyco import race
from .helpers import run_in_loop


def coro(delay=1):
    @asyncio.coroutine
    def wrapper():
        yield from asyncio.sleep(delay)
        return delay
    return wrapper


def test_race():
    faster = run_in_loop(
        race((coro(0.8), coro(0.5), coro(1), coro(3), coro(0.2)))
    )
    assert faster == 0.2


def test_race_timeout():
    faster = run_in_loop(
        race((coro(1), coro(1)), timeout=0.1)
    )
    assert faster is None


def test_race_invalid_input():
    try:
        run_in_loop(race(None))
    except TypeError:
        pass
    else:
        raise RuntimeError('must raise exception')
