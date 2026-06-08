"""
    .. module:: segment
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: DTOs for NSX-T segments (logical switches).

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from ccai.restclient.base.schemaobject import SchemaObject
from ccai.restclient.base.schemafield import Field


class SegmentSummary(SchemaObject):
    """
        Compact summary of an NSX-T segment / logical switch.
    """
    id = Field(str, required=True)
    display_name = Field(str, required=True)
    path = Field(str, required=False)
    resource_type = Field(str, required=False)
    connectivity_path = Field(str, required=False)
    transport_zone_path = Field(str, required=False)
    vlan_ids = Field(list, required=False)


class SegmentInfo(SchemaObject):
    """
        Detailed view of an NSX-T segment including subnet bindings.
    """
    id = Field(str, required=True)
    display_name = Field(str, required=True)
    path = Field(str, required=False)
    resource_type = Field(str, required=False)
    connectivity_path = Field(str, required=False)
    transport_zone_path = Field(str, required=False)
    vlan_ids = Field(list, required=False)
    subnets = Field(list, required=False)
    advanced_config = Field(dict, required=False)
