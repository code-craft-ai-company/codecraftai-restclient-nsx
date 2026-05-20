"""
    Tests for :class:`NsxRealizationHandle` poll loop, using injected
    status fetchers / clocks so no network or wall-clock is involved.
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


import pytest

from automojo.errors.exceptions import SemanticError
from automojo.interfaces.itaskhandle import ITaskHandle, TaskState

from automojo.interop.nsx.aspectsnsx import AspectsNsx
from automojo.interop.nsx.nsxrealizationhandle import (
    NsxRealizationError,
    NsxRealizationHandle,
    NsxRealizationTimeoutError,
    RealizationState,
)


def _scripted_fetcher(states):
    """
        Build a status fetcher that yields the supplied states in order.
    """
    queue = list(states)

    def fetcher(intent_path):
        if len(queue) > 1:
            state = queue.pop(0)
        else:
            state = queue[0]
        return {"state": state, "intent_path": intent_path}

    return fetcher


def _fake_clock():
    """
        Build a monotonic fake clock advancing 1.0s per call.
    """
    ticks = {"now": 0.0}

    def clock():
        value = ticks["now"]
        ticks["now"] = ticks["now"] + 1.0
        return value

    return clock


def test_handle_is_itaskhandle() -> None:
    handle = NsxRealizationHandle(
        intent_path="/infra/segments/seg-a",
        client=None,
        status_fetcher=_scripted_fetcher(["REALIZED"]),
    )
    assert isinstance(handle, ITaskHandle)
    return


def test_wait_succeeds_on_realized() -> None:
    handle = NsxRealizationHandle(
        intent_path="/infra/segments/seg-a",
        client=None,
        status_fetcher=_scripted_fetcher(
            ["UNREALIZED", "IN_PROGRESS", "REALIZED"]
        ),
        sleeper=lambda _interval: None,
        clock=_fake_clock(),
    )
    result = handle.wait(aspects=AspectsNsx())
    assert result.state == TaskState.SUCCEEDED
    assert handle.is_done() is True
    assert handle.transition_log_count == 3
    return


def test_wait_raises_on_error_state() -> None:
    handle = NsxRealizationHandle(
        intent_path="/infra/segments/seg-a",
        client=None,
        status_fetcher=_scripted_fetcher(["ERROR"]),
        sleeper=lambda _interval: None,
        clock=_fake_clock(),
    )
    with pytest.raises(NsxRealizationError):
        handle.wait(aspects=AspectsNsx())
    return


def test_wait_times_out() -> None:
    handle = NsxRealizationHandle(
        intent_path="/infra/segments/seg-a",
        client=None,
        status_fetcher=_scripted_fetcher(["IN_PROGRESS"]),
        sleeper=lambda _interval: None,
        clock=_fake_clock(),
    )
    aspects = AspectsNsx(completion_timeout=3.0, completion_interval=1.0)
    with pytest.raises(NsxRealizationTimeoutError):
        handle.wait(aspects=aspects)
    return


def test_wait_rejects_nonpositive_interval() -> None:
    handle = NsxRealizationHandle(
        intent_path="/infra/segments/seg-a",
        client=None,
        status_fetcher=_scripted_fetcher(["REALIZED"]),
    )
    aspects = AspectsNsx(completion_interval=0.0)
    with pytest.raises(SemanticError):
        handle.wait(aspects=aspects)
    return


def test_status_observes_state() -> None:
    handle = NsxRealizationHandle(
        intent_path="/infra/segments/seg-a",
        client=None,
        status_fetcher=_scripted_fetcher(["IN_PROGRESS"]),
    )
    info = handle.status(aspects=AspectsNsx())
    assert info.state == "IN_PROGRESS"
    assert handle.is_done() is False
    return


def test_cancel_noop_when_terminal() -> None:
    handle = NsxRealizationHandle(
        intent_path="/infra/segments/seg-a",
        client=None,
        status_fetcher=_scripted_fetcher(["REALIZED"]),
    )
    handle.status(aspects=AspectsNsx())
    assert handle.cancel(aspects=AspectsNsx()) is None
    return


def test_cancel_raises_when_active() -> None:
    handle = NsxRealizationHandle(
        intent_path="/infra/segments/seg-a",
        client=None,
        status_fetcher=_scripted_fetcher(["IN_PROGRESS"]),
    )
    handle.status(aspects=AspectsNsx())
    with pytest.raises(NotImplementedError):
        handle.cancel(aspects=AspectsNsx())
    return


def test_orphaned_is_terminal() -> None:
    assert RealizationState.ORPHANED in __import__(
        "automojo.interop.nsx.nsxrealizationhandle",
        fromlist=["TERMINAL_STATES"],
    ).TERMINAL_STATES
    return
