"""
    .. module:: aspectsnsx
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Provides the :class:`AspectsNsx` subclass and the
        ``DEFAULT_NSX_ASPECTS`` instance used by every call on
        :class:`NsxClient` and its API groups.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


import logging

from typing import Optional

from automojo.restclient.base.aspectsrest import (
    AspectsRest,
    ActionPattern,
    LoggingPattern,
)


class AspectsNsx(AspectsRest):
    """
        NSX-T-specialised :class:`AspectsRest`.

        The subclass exists so callers can annotate ``aspects: AspectsNsx``
        for clarity at call sites and so NSX-specific behaviour (such as
        realization-state poll cadence) can evolve without churning the
        public type signature on every group method.
    """

    def __init__(
        self,
        *,
        action_pattern: ActionPattern = ActionPattern.SINGLE_CALL,
        completion_timeout: float = 120.0,
        completion_interval: float = 3.0,
        connection_timeout: float = 16.0,
        inactivity_timeout: float = 60.0,
        monitor_delay: float = 30.0,
        logging_pattern: int = LoggingPattern.ALL_RESULTS,
        retry_logging_interval: int = 5,
        must_connect: bool = False,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """
            Initialise an NSX-flavoured aspects bundle.

            :param action_pattern: Action pattern for the call.
            :param completion_timeout: Overall completion timeout in
                seconds.  NSX realization can take longer than vCenter
                tasks, hence the larger default.
            :param completion_interval: Poll interval for waiters in
                seconds.
            :param connection_timeout: TCP connection establishment
                timeout.
            :param inactivity_timeout: Per-read inactivity timeout.
            :param monitor_delay: Delay before background monitoring
                begins.
            :param logging_pattern: Logging pattern controlling
                verbosity.
            :param retry_logging_interval: Cadence at which retry
                attempts log.
            :param must_connect: Whether a connection failure is fatal.
            :param logger: Optional logger override.

            :returns: ``None``
        """
        super().__init__(
            action_pattern=action_pattern,
            completion_timeout=completion_timeout,
            completion_interval=completion_interval,
            connection_timeout=connection_timeout,
            inactivity_timeout=inactivity_timeout,
            monitor_delay=monitor_delay,
            logging_pattern=logging_pattern,
            retry_logging_interval=retry_logging_interval,
            must_connect=must_connect,
            logger=logger,
        )
        return


DEFAULT_NSX_ASPECTS = AspectsNsx()
