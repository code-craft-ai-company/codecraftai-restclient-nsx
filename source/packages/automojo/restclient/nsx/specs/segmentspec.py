"""
    .. module:: segmentspec
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Request spec for creating or updating an NSX-T segment.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Dict, List, Optional


class SegmentSpec:
    """
        Typed request spec for the segment ``PATCH`` body.
    """

    def __init__(
        self,
        *,
        display_name: str,
        connectivity_path: Optional[str] = None,
        transport_zone_path: Optional[str] = None,
        vlan_ids: Optional[List[int]] = None,
        subnets: Optional[List[Dict[str, object]]] = None,
    ) -> None:
        """
            Initialise a :class:`SegmentSpec`.

            :param display_name: Human-readable name for the segment.
            :param connectivity_path: Policy path of the gateway the
                segment attaches to.
            :param transport_zone_path: Policy path of the transport
                zone.
            :param vlan_ids: VLAN ids for a VLAN-backed segment.
            :param subnets: Subnet binding dictionaries.

            :returns: ``None``
        """
        self._display_name = display_name
        self._connectivity_path = connectivity_path
        self._transport_zone_path = transport_zone_path
        self._vlan_ids = vlan_ids
        self._subnets = subnets
        return

    def to_dict(self) -> Dict[str, object]:
        """
            Render the spec as the NSX-T policy request body.

            :returns: The request body dictionary.
        """
        rtnval: Dict[str, object] = {"display_name": self._display_name}
        if self._connectivity_path is not None:
            rtnval["connectivity_path"] = self._connectivity_path
        if self._transport_zone_path is not None:
            rtnval["transport_zone_path"] = self._transport_zone_path
        if self._vlan_ids is not None:
            rtnval["vlan_ids"] = list(self._vlan_ids)
        if self._subnets is not None:
            rtnval["subnets"] = list(self._subnets)
        return rtnval
