"""
    .. module:: security
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: DTOs for NSX-T security groups and distributed firewall.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from ccai.restclient.base.schemaobject import SchemaObject
from ccai.restclient.base.schemafield import Field


class SecurityGroupSummary(SchemaObject):
    """
        Summary of an NSX-T policy security group (``Group``).
    """
    id = Field(str, required=True)
    display_name = Field(str, required=True)
    path = Field(str, required=False)
    resource_type = Field(str, required=False)
    expression = Field(list, required=False)


class DfwRule(SchemaObject):
    """
        A single distributed-firewall rule within a security policy.
    """
    id = Field(str, required=True)
    display_name = Field(str, required=True)
    path = Field(str, required=False)
    resource_type = Field(str, required=False)
    action = Field(str, required=False)
    source_groups = Field(list, required=False)
    destination_groups = Field(list, required=False)
    services = Field(list, required=False)
    direction = Field(str, required=False)
    sequence_number = Field(int, required=False)


class DfwPolicy(SchemaObject):
    """
        A distributed-firewall security policy (rule container).
    """
    id = Field(str, required=True)
    display_name = Field(str, required=True)
    path = Field(str, required=False)
    resource_type = Field(str, required=False)
    category = Field(str, required=False)
    rules = Field(list, required=False)
