"""
    .. module:: gatewayspec
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Request specs for NSX-T Tier-0 and Tier-1 gateways.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import Dict, List, Optional


class T0GatewaySpec:
    """
        Typed request spec for the Tier-0 gateway ``PATCH`` body.
    """

    def __init__(
        self,
        *,
        display_name: str,
        ha_mode: Optional[str] = None,
        failover_mode: Optional[str] = None,
    ) -> None:
        """
            Initialise a :class:`T0GatewaySpec`.

            :param display_name: Human-readable name for the gateway.
            :param ha_mode: High-availability mode (``ACTIVE_ACTIVE`` /
                ``ACTIVE_STANDBY``).
            :param failover_mode: Failover mode for the gateway.

            :returns: ``None``
        """
        self._display_name = display_name
        self._ha_mode = ha_mode
        self._failover_mode = failover_mode
        return

    def to_dict(self) -> Dict[str, object]:
        """
            Render the spec as the NSX-T policy request body.

            :returns: The request body dictionary.
        """
        rtnval: Dict[str, object] = {"display_name": self._display_name}
        if self._ha_mode is not None:
            rtnval["ha_mode"] = self._ha_mode
        if self._failover_mode is not None:
            rtnval["failover_mode"] = self._failover_mode
        return rtnval


class T1GatewaySpec:
    """
        Typed request spec for the Tier-1 gateway ``PATCH`` body.
    """

    def __init__(
        self,
        *,
        display_name: str,
        tier0_path: Optional[str] = None,
        route_advertisement_types: Optional[List[str]] = None,
    ) -> None:
        """
            Initialise a :class:`T1GatewaySpec`.

            :param display_name: Human-readable name for the gateway.
            :param tier0_path: Policy path of the parent Tier-0 gateway.
            :param route_advertisement_types: Route advertisement type
                strings.

            :returns: ``None``
        """
        self._display_name = display_name
        self._tier0_path = tier0_path
        self._route_advertisement_types = route_advertisement_types
        return

    def to_dict(self) -> Dict[str, object]:
        """
            Render the spec as the NSX-T policy request body.

            :returns: The request body dictionary.
        """
        rtnval: Dict[str, object] = {"display_name": self._display_name}
        if self._tier0_path is not None:
            rtnval["tier0_path"] = self._tier0_path
        if self._route_advertisement_types is not None:
            rtnval["route_advertisement_types"] = list(
                self._route_advertisement_types
            )
        return rtnval
