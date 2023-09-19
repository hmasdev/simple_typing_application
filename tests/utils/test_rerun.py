import asyncio
import pytest
from simple_typing_application.utils.rerun import (
    rerun_deco,
    MaxRetryError
)


def test_rerun_deco():

    # preparation
    execution_ctr: int = 0
    expected: int = 3
    max_retry: int = 4

    # no exception case
    @rerun_deco(max_retry=max_retry)
    def func_wo_error():
        nonlocal execution_ctr
        execution_ctr += 1
        return expected

    execution_ctr = 0
    actual = func_wo_error()
    assert actual == expected
    assert execution_ctr == 1  # no retry

    # 2 exceptions case
    @rerun_deco(max_retry=max_retry)
    def func_w_errors():
        nonlocal execution_ctr
        if execution_ctr < 2:
            execution_ctr += 1
            raise Exception(f"execution count: {execution_ctr}")
        else:
            execution_ctr += 1
            return expected

    execution_ctr = 0
    actual = func_w_errors()
    assert actual == expected
    assert execution_ctr == 3  # 2 retries

    # always raise errors case
    @rerun_deco(max_retry=max_retry)
    def func_always_raise_errors():
        nonlocal execution_ctr
        execution_ctr += 1
        raise Exception(f"execution count: {execution_ctr}")

    execution_ctr = 0
    with pytest.raises(MaxRetryError):
        func_always_raise_errors()
    assert execution_ctr == max_retry  # max_retry retries


def test_rerun_deco_async():

    # preparation
    execution_ctr: int = 0
    expected: int = 3
    max_retry: int = 4

    # no exception case
    @rerun_deco(max_retry=max_retry)
    async def func_wo_error():
        nonlocal execution_ctr
        execution_ctr += 1
        return expected

    execution_ctr = 0
    actual = asyncio.run(func_wo_error())
    assert actual == expected
    assert execution_ctr == 1  # no retry

    # 2 exceptions case
    @rerun_deco(max_retry=max_retry)
    async def func_w_errors():
        nonlocal execution_ctr
        if execution_ctr < 2:
            execution_ctr += 1
            raise Exception(f"execution count: {execution_ctr}")
        else:
            execution_ctr += 1
            return expected

    execution_ctr = 0
    actual = asyncio.run(func_w_errors())
    assert actual == expected
    assert execution_ctr == 3  # 2 retries

    # always raise errors case
    @rerun_deco(max_retry=max_retry)
    async def func_always_raise_errors():
        nonlocal execution_ctr
        execution_ctr += 1
        raise Exception(f"execution count: {execution_ctr}")

    execution_ctr = 0
    with pytest.raises(MaxRetryError):
        asyncio.run(func_always_raise_errors())
    assert execution_ctr == max_retry  # max_retry retries


def test_rerun_deco_with_callback():

    # preparation
    execution_ctr: int = 0
    expected: int = 3
    max_retry: int = 4

    def callback():
        nonlocal execution_ctr
        execution_ctr += 1

    @rerun_deco(max_retry=max_retry, callback=callback)
    def func_w_errors():
        nonlocal execution_ctr
        if execution_ctr < 2:
            # 2 exceptions case
            raise Exception(f"execution count: {execution_ctr}")
        else:
            return expected

    execution_ctr = 0
    actual = func_w_errors()
    assert actual == expected
    assert execution_ctr + 1 == 3  # 2 retries
    # NOTE: callback is called when func raises an exception


def test_rerun_deco_async_with_callback():

    # preparation
    execution_ctr: int = 0
    expected: int = 3
    max_retry: int = 4

    def callback():
        nonlocal execution_ctr
        execution_ctr += 1

    @rerun_deco(max_retry=max_retry, callback=callback)
    async def func_w_errors():
        nonlocal execution_ctr
        if execution_ctr < 2:
            # 2 exceptions case
            raise Exception(f"execution count: {execution_ctr}")
        else:
            return expected

    execution_ctr = 0
    actual = asyncio.run(func_w_errors())
    assert actual == expected
    assert execution_ctr + 1 == 3  # 2 retries
    # NOTE: callback is called when func raises an exception


def test_rerun_deco_as_decorator():
    # preparation
    execution_ctr: int = 0
    expected: int = 3

    # 2 exceptions case
    @rerun_deco
    def func_w_errors():
        nonlocal execution_ctr
        if execution_ctr < 2:
            execution_ctr += 1
            raise Exception(f"execution count: {execution_ctr}")
        else:
            execution_ctr += 1
            return expected

    execution_ctr = 0
    actual = func_w_errors()
    assert actual == expected
    assert execution_ctr == 3  # 2 retries
