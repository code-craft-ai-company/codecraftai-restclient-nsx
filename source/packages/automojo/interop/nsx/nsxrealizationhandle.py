"""
    .. module:: nsxrealizationhandle
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Provides :class:`NsxRealizationHandle`, the sync-poll
        Aspects-driven handle returned by every mutating NSX-T policy
        call.  Conforms structurally to :class:`ITaskHandle` from
        ``automojo-interfaces``.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


import os
import time
import logging

from enum import Enum
from typing import Callable, Optional, TYPE_CHECKING

from automojo.errors.exceptions import SemanticError
from automojo.interfaces.itaskhandle import (
    ITaskHandle,
    TaskResult,
    TaskState as IfaceTaskState,
)

from automojo.interop.nsx.model.realization import RealizationStateInfo


if TYPE_CHECKING:
    from automojo.interop.nsx.aspectsnsx import AspectsNsx
    from automojo.interop.nsx.nsxclient import NsxClient


class RealizationState(str, Enum):
    """
        NSX-T policy intent realization-state values.

        ``UNREALIZED`` and ``IN_PROGRESS`` are non-terminal.
        ``REALIZED``, ``ERROR``, and ``ORPHANED`` are terminal.
    """
    UNREALIZED = "UNREALIZED"
    IN_PROGRESS = "IN_PROGRESS"
    REALIZED = "REALIZED"
    ERROR = "ERROR"
    ORPHANED = "ORPHANED"


TERMINAL_STATES = frozenset({
    RealizationState.REALIZED,
    RealizationState.ERROR,
    RealizationState.ORPHANED,
})


_IFACE_STATE_MAP = {
    RealizationState.UNREALIZED: IfaceTaskState.PENDING,
    RealizationState.IN_PROGRESS: IfaceTaskState.RUNNING,
    RealizationState.REALIZED: IfaceTaskState.SUCCEEDED,
    RealizationState.ERROR: IfaceTaskState.FAILED,
    RealizationState.ORPHANED: IfaceTaskState.FAILED,
}


class NsxRealizationError(Exception):
    """
        Raised when a policy intent reaches ``ERROR`` or ``ORPHANED``.
    """

    def __init__(self, message: str, info: RealizationStateInfo) -> None:
        """
            Initialise with a message and the failing realization info.

            :param message: Multi-line error text.
            :param info: RealizationStateInfo at the time of failure.

            :returns: ``None``
        """
        super().__init__(message)
        self.info = info
        return


class NsxRealizationTimeoutError(TimeoutError):
    """
        Raised when ``wait`` exceeds its aspect timeout.
    """

    def __init__(
        self,
        message: str,
        info: Optional[RealizationStateInfo],
    ) -> None:
        """
            Initialise with a message and the last-observed info.

            :param message: Multi-line timeout text.
            :param info: RealizationStateInfo at the time of the
                timeout, possibly ``None`` when no observation was made.

            :returns: ``None``
        """
        super().__init__(message)
        self.info = info
        return


def _parse_realization_info(*, payload: dict) -> RealizationStateInfo:
    """
        Parse a raw NSX-T realization-state payload into a typed DTO.

        The policy API may report the consolidated state under either
        ``state`` or ``publish_status`` depending on the endpoint; both
        are normalised here.

        :param payload: The raw status payload as a dictionary.

        :returns: A parsed :class:`RealizationStateInfo`.
    """
    raw_state = payload.get("state")
    if raw_state is None:
        raw_state = payload.get("consolidated_status")
    if raw_state is None:
        raw_state = "IN_PROGRESS"

    rtnval = RealizationStateInfo(
        state=raw_state,
        publish_status=payload.get("publish_status"),
        intent_path=payload.get("intent_path"),
        entity_type=payload.get("entity_type"),
        alarms=payload.get("alarms"),
    )
    return rtnval


class NsxRealizationHandle:
    """
        Synchronous, Aspects-driven handle on an NSX-T policy intent's
        realization onto the enforcement plane.

        NSX-T policy mutations differ from vCenter tasks: the
        ``PATCH``/``PUT`` returns ``200`` immediately and the intent is
        realized asynchronously.  This handle polls the realization-state
        endpoint for the intent path until a terminal state is reached.

        The handle conforms structurally to
        :class:`automojo.interfaces.itaskhandle.ITaskHandle` so it is
        recognised by ``isinstance(handle, ITaskHandle)``.
    """

    REALIZATION_LEAF = "/policy/api/v1/infra/realized-state/status"

    def __init__(
        self,
        *,
        intent_path: str,
        client: "NsxClient",
        status_fetcher: Optional[Callable[[str], dict]] = None,
        sleeper: Optional[Callable[[float], None]] = None,
        clock: Optional[Callable[[], float]] = None,
    ) -> None:
        """
            Initialise a realization handle.

            :param intent_path: Policy path of the mutated intent
                object.
            :param client: Owning :class:`NsxClient`; supplies HTTP.
            :param status_fetcher: Optional override for the function
                that retrieves the raw realization-status dict for a
                given intent path.  Used by tests to drive scripted
                state sequences without a network round-trip.
            :param sleeper: Optional override for ``time.sleep``;
                injected by tests to keep the poll loop deterministic.
            :param clock: Optional override for ``time.monotonic``;
                injected by tests.

            :returns: ``None``
        """
        self._intent_path = intent_path
        self._client = client
        self._status_fetcher = status_fetcher
        self._sleeper = sleeper
        self._clock = clock
        self._last_observed_state: Optional[RealizationState] = None
        self._last_info: Optional[RealizationStateInfo] = None
        self._transition_log_count: int = 0
        return

    @property
    def transition_log_count(self) -> int:
        """
            Number of state-transition log lines emitted by ``wait``.

            :returns: The integer transition-log counter.
        """
        rtnval = self._transition_log_count
        return rtnval

    def task_id(self) -> str:
        """
            Returns the intent path that identifies this realization.

            :returns: The intent path captured at construction.
        """
        rtnval = self._intent_path
        return rtnval

    def is_done(self) -> bool:
        """
            Indicates if the most recently observed state is terminal.

            :returns: ``True`` when the last observation was terminal.
        """
        rtnval = False
        if self._last_observed_state is not None:
            if self._last_observed_state in TERMINAL_STATES:
                rtnval = True
        return rtnval

    def status(self, *, aspects: "AspectsNsx") -> RealizationStateInfo:
        """
            Fetch and parse the current realization state as a fresh
            GET.

            :param aspects: Behaviour controls for the GET.

            :returns: A freshly observed :class:`RealizationStateInfo`.
        """
        payload = self._fetch_status(aspects=aspects)
        info = _parse_realization_info(payload=payload)

        observed_state: Optional[RealizationState] = None
        try:
            observed_state = RealizationState(info.state)
        except ValueError:
            observed_state = RealizationState.IN_PROGRESS

        self._last_observed_state = observed_state
        self._last_info = info
        return info

    def wait(self, *, aspects: "AspectsNsx") -> TaskResult:
        """
            Poll until the intent reaches a terminal realization state,
            raising on failure or timeout.

            Strict-timeout-gate-at-top-of-iteration: the elapsed-time
            check runs before each status GET so a long-running GET
            cannot blow past the aspect timeout.

            :param aspects: Behaviour controls.  ``completion_interval``
                is the poll interval; ``completion_timeout`` is the
                wall-clock cap.

            :returns: A :class:`TaskResult` describing the terminal
                state.

            :raises: NsxRealizationError, NsxRealizationTimeoutError,
                SemanticError
        """
        interval = aspects.completion_interval
        timeout = aspects.completion_timeout

        if interval <= 0:
            err_msg_lines = [
                "NsxRealizationHandle.wait requires "
                "aspects.completion_interval > 0.",
                "GOT interval={}".format(interval),
            ]
            err_msg = os.linesep.join(err_msg_lines)
            raise SemanticError(err_msg)

        if timeout <= 0:
            err_msg_lines = [
                "NsxRealizationHandle.wait requires "
                "aspects.completion_timeout > 0.",
                "GOT timeout={}".format(timeout),
            ]
            err_msg = os.linesep.join(err_msg_lines)
            raise SemanticError(err_msg)

        clock = self._clock
        if clock is None:
            clock = time.monotonic

        sleeper = self._sleeper
        if sleeper is None:
            sleeper = time.sleep

        logger = aspects.logger
        if logger is None:
            logger = logging.getLogger("automojo.interop.nsx")

        started = clock()
        last_state: Optional[RealizationState] = None
        last_info: Optional[RealizationStateInfo] = None

        rtnval: Optional[TaskResult] = None

        while True:

            elapsed = clock() - started
            if elapsed > timeout:
                err_msg_lines = [
                    "NsxRealizationHandle.wait timed out.",
                    "INTENT: {}".format(self._intent_path),
                    "TIMEOUT: {}s".format(timeout),
                    "ELAPSED: {}s".format(elapsed),
                    "LAST STATE: {}".format(
                        last_state.value if last_state is not None
                        else "<none>"
                    ),
                ]
                err_msg = os.linesep.join(err_msg_lines)
                raise NsxRealizationTimeoutError(err_msg, info=last_info)

            info = self.status(aspects=aspects)
            last_info = info

            observed_state = self._last_observed_state

            if observed_state != last_state:
                logger.info(
                    "nsx intent %s realization state: %s",
                    self._intent_path,
                    info.state,
                )
                self._transition_log_count = self._transition_log_count + 1
                last_state = observed_state

            if observed_state in TERMINAL_STATES:
                if observed_state == RealizationState.REALIZED:
                    rtnval = TaskResult(
                        task_id=self._intent_path,
                        state=_IFACE_STATE_MAP[observed_state],
                        progress=100,
                        error=None,
                        payload=None,
                    )
                    break

                err_msg_lines = [
                    "NSX-T intent reached a non-success terminal state.",
                    "INTENT: {}".format(self._intent_path),
                    "STATE: {}".format(info.state),
                ]
                if info.alarms is not None:
                    err_msg_lines.append("ALARMS: {!r}".format(info.alarms))
                err_msg = os.linesep.join(err_msg_lines)
                raise NsxRealizationError(err_msg, info=info)

            sleeper(interval)

        return rtnval

    def cancel(self, *, aspects: "AspectsNsx") -> None:
        """
            NSX-T policy intent realization cannot be cancelled once the
            intent has been accepted by the manager; the intent must be
            deleted instead.

            Per the :class:`ITaskHandle` contract, this method is a
            no-op when the intent has already reached a terminal state,
            and otherwise raises :class:`NotImplementedError`.

            :param aspects: Behaviour controls (unused; carried for
                interface symmetry).

            :returns: ``None``

            :raises: NotImplementedError
        """
        _ = aspects
        if self._last_observed_state is not None:
            if self._last_observed_state in TERMINAL_STATES:
                return None

        err_msg_lines = [
            "NSX-T policy intent realization cannot be cancelled.",
            "INTENT: {}".format(self._intent_path),
            "REMEDY: delete the intent object to revert it.",
        ]
        err_msg = os.linesep.join(err_msg_lines)
        raise NotImplementedError(err_msg)

    def _fetch_status(self, *, aspects: "AspectsNsx") -> dict:
        """
            Fetch the raw realization-status dict for the intent path.

            :param aspects: Behaviour controls for the GET.

            :returns: The raw payload as a dictionary.
        """
        fetcher = self._status_fetcher
        if fetcher is not None:
            rtnval = fetcher(self._intent_path)
            return rtnval

        client = self._client
        status_url = client.build_url(leaf=self.REALIZATION_LEAF)
        session = client.ensure_session(aspects=aspects)
        resp = session.get(
            status_url,
            params={"intent_path": self._intent_path},
            timeout=aspects.completion_timeout,
        )
        rtnval = resp.json()
        return rtnval


# Runtime conformance attestation.  ``ITaskHandle`` is a
# ``@runtime_checkable`` Protocol, so isinstance() works structurally;
# this assignment exists purely to make the structural relationship
# obvious to readers and to lock the import into the module.
_ITASKHANDLE_PROTOCOL = ITaskHandle
