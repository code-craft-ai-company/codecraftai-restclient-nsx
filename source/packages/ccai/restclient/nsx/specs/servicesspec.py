"""
    .. module:: servicesspec
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Request specs for NSX-T NAT rules and load balancers.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import Dict, List, Optional


class NatRuleSpec:
    """
        Typed request spec for a NAT rule ``PATCH`` body.
    """

    def __init__(
        self,
        *,
        display_name: str,
        action: str,
        source_network: Optional[str] = None,
        destination_network: Optional[str] = None,
        translated_network: Optional[str] = None,
        enabled: bool = True,
    ) -> None:
        """
            Initialise a :class:`NatRuleSpec`.

            :param display_name: Human-readable name for the rule.
            :param action: NAT action (``SNAT`` / ``DNAT`` /
                ``REFLEXIVE`` / ``NO_SNAT`` / ``NO_DNAT``).
            :param source_network: Source CIDR/IP the rule matches.
            :param destination_network: Destination CIDR/IP the rule
                matches.
            :param translated_network: Translated CIDR/IP.
            :param enabled: Whether the rule is enabled.

            :returns: ``None``
        """
        self._display_name = display_name
        self._action = action
        self._source_network = source_network
        self._destination_network = destination_network
        self._translated_network = translated_network
        self._enabled = enabled
        return

    def to_dict(self) -> Dict[str, object]:
        """
            Render the spec as the NSX-T policy request body.

            :returns: The request body dictionary.
        """
        rtnval: Dict[str, object] = {
            "display_name": self._display_name,
            "action": self._action,
            "enabled": self._enabled,
        }
        if self._source_network is not None:
            rtnval["source_network"] = self._source_network
        if self._destination_network is not None:
            rtnval["destination_network"] = self._destination_network
        if self._translated_network is not None:
            rtnval["translated_network"] = self._translated_network
        return rtnval


class LoadBalancerSpec:
    """
        Typed request spec for a load balancer service ``PATCH`` body.
    """

    def __init__(
        self,
        *,
        display_name: str,
        connectivity_path: Optional[str] = None,
        size: str = "SMALL",
        enabled: bool = True,
    ) -> None:
        """
            Initialise a :class:`LoadBalancerSpec`.

            :param display_name: Human-readable name for the LB service.
            :param connectivity_path: Policy path of the Tier-1 gateway
                the LB attaches to.
            :param size: LB sizing tier (``SMALL`` / ``MEDIUM`` /
                ``LARGE``).
            :param enabled: Whether the LB service is enabled.

            :returns: ``None``
        """
        self._display_name = display_name
        self._connectivity_path = connectivity_path
        self._size = size
        self._enabled = enabled
        return

    def to_dict(self) -> Dict[str, object]:
        """
            Render the spec as the NSX-T policy request body.

            :returns: The request body dictionary.
        """
        rtnval: Dict[str, object] = {
            "display_name": self._display_name,
            "size": self._size,
            "enabled": self._enabled,
        }
        if self._connectivity_path is not None:
            rtnval["connectivity_path"] = self._connectivity_path
        return rtnval


class LbVirtualServerSpec:
    """
        Typed request spec for a load balancer virtual server ``PATCH``
        body.
    """

    def __init__(
        self,
        *,
        display_name: str,
        ip_address: str,
        ports: List[str],
        pool_path: Optional[str] = None,
    ) -> None:
        """
            Initialise a :class:`LbVirtualServerSpec`.

            :param display_name: Human-readable name.
            :param ip_address: Virtual IP address.
            :param ports: List of listener port strings.
            :param pool_path: Policy path of the backing server pool.

            :returns: ``None``
        """
        self._display_name = display_name
        self._ip_address = ip_address
        self._ports = ports
        self._pool_path = pool_path
        return

    def to_dict(self) -> Dict[str, object]:
        """
            Render the spec as the NSX-T policy request body.

            :returns: The request body dictionary.
        """
        rtnval: Dict[str, object] = {
            "display_name": self._display_name,
            "ip_address": self._ip_address,
            "ports": list(self._ports),
        }
        if self._pool_path is not None:
            rtnval["pool_path"] = self._pool_path
        return rtnval


class LbPoolSpec:
    """
        Typed request spec for a load balancer server pool ``PATCH``
        body.
    """

    def __init__(
        self,
        *,
        display_name: str,
        algorithm: str = "ROUND_ROBIN",
        members: Optional[List[Dict[str, object]]] = None,
    ) -> None:
        """
            Initialise a :class:`LbPoolSpec`.

            :param display_name: Human-readable name.
            :param algorithm: Load-balancing algorithm.
            :param members: Pool member dictionaries.

            :returns: ``None``
        """
        self._display_name = display_name
        self._algorithm = algorithm
        self._members = members
        return

    def to_dict(self) -> Dict[str, object]:
        """
            Render the spec as the NSX-T policy request body.

            :returns: The request body dictionary.
        """
        rtnval: Dict[str, object] = {
            "display_name": self._display_name,
            "algorithm": self._algorithm,
        }
        if self._members is not None:
            rtnval["members"] = list(self._members)
        return rtnval
