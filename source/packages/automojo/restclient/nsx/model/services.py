"""
    .. module:: services
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: DTOs for NSX-T NAT rules and load balancers.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from automojo.restclient.base.schemaobject import SchemaObject
from automojo.restclient.base.schemafield import Field


class NatRule(SchemaObject):
    """
        A NAT rule scoped to a Tier-0 or Tier-1 gateway.
    """
    id = Field(str, required=True)
    display_name = Field(str, required=True)
    path = Field(str, required=False)
    resource_type = Field(str, required=False)
    action = Field(str, required=False)
    source_network = Field(str, required=False)
    destination_network = Field(str, required=False)
    translated_network = Field(str, required=False)
    enabled = Field(bool, required=False)


class LoadBalancerSummary(SchemaObject):
    """
        Summary of an NSX-T load balancer service.
    """
    id = Field(str, required=True)
    display_name = Field(str, required=True)
    path = Field(str, required=False)
    resource_type = Field(str, required=False)
    connectivity_path = Field(str, required=False)
    size = Field(str, required=False)
    enabled = Field(bool, required=False)


class LbVirtualServer(SchemaObject):
    """
        An NSX-T load balancer virtual server.
    """
    id = Field(str, required=True)
    display_name = Field(str, required=True)
    path = Field(str, required=False)
    resource_type = Field(str, required=False)
    ip_address = Field(str, required=False)
    ports = Field(list, required=False)
    pool_path = Field(str, required=False)


class LbPool(SchemaObject):
    """
        An NSX-T load balancer server pool.
    """
    id = Field(str, required=True)
    display_name = Field(str, required=True)
    path = Field(str, required=False)
    resource_type = Field(str, required=False)
    algorithm = Field(str, required=False)
    members = Field(list, required=False)
