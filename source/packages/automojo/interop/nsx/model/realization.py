"""
    .. module:: realization
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: DTO for an NSX-T policy realization-state observation.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from automojo.restclient.base.schemaobject import SchemaObject
from automojo.restclient.base.schemafield import Field


class RealizationStateInfo(SchemaObject):
    """
        A single observation of an NSX-T policy intent's realization
        state on the enforcement plane.

        NSX-T policy mutations are accepted by the manager immediately
        (the ``PATCH``/``PUT`` returns ``200``) but the intent is then
        realized asynchronously onto the enforcement plane.  The
        ``state`` field reports progress toward realization.
    """
    state = Field(str, required=True)
    publish_status = Field(str, required=False)
    intent_path = Field(str, required=False)
    entity_type = Field(str, required=False)
    alarms = Field(list, required=False)
