"""
    .. module:: gateway
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: DTOs for NSX-T Tier-0 and Tier-1 gateways.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from automojo.restclient.base.schemaobject import SchemaObject
from automojo.restclient.base.schemafield import Field


class T0GatewaySummary(SchemaObject):
    """
        Summary of an NSX-T Tier-0 gateway (provider/north-south router).
    """
    id = Field(str, required=True)
    display_name = Field(str, required=True)
    path = Field(str, required=False)
    resource_type = Field(str, required=False)
    ha_mode = Field(str, required=False)
    failover_mode = Field(str, required=False)


class T1GatewaySummary(SchemaObject):
    """
        Summary of an NSX-T Tier-1 gateway (tenant/east-west router).
    """
    id = Field(str, required=True)
    display_name = Field(str, required=True)
    path = Field(str, required=False)
    resource_type = Field(str, required=False)
    tier0_path = Field(str, required=False)
    route_advertisement_types = Field(list, required=False)
