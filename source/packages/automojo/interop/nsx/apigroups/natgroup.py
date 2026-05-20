"""
    .. module:: natgroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: NAT rules API group for :class:`NsxClient`.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import List

from automojo.interop.nsx.apigroups.basegroup import BaseGroup
from automojo.interop.nsx.aspectsnsx import AspectsNsx, DEFAULT_NSX_ASPECTS
from automojo.interop.nsx.model.services import NatRule
from automojo.interop.nsx.nsxrealizationhandle import NsxRealizationHandle
from automojo.interop.nsx.specs.servicesspec import NatRuleSpec


# NSX-T policy NAT rules are scoped to a Tier-1 gateway and a NAT
# section; ``USER`` is the section operators populate.
_USER_NAT = "USER"


class NatGroup(BaseGroup):
    """
        Operations on NSX-T NAT rules scoped to a Tier-1 gateway
        (``/policy/api/v1/infra/tier-1s/{id}/nat/USER/nat-rules``).
    """

    BASE_LEAF = "/policy/api/v1/infra/tier-1s"

    def list(
        self,
        *,
        gateway_id: str,
        nat_section: str = _USER_NAT,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> List[NatRule]:
        """
            List every NAT rule on a Tier-1 gateway NAT section.

            :param gateway_id: The Tier-1 gateway identifier.
            :param nat_section: The NAT section id (default ``USER``).
            :param aspects: Behaviour controls.

            :returns: List of :class:`NatRule`.
        """
        url = self.compose_url(
            parts=[gateway_id, "nat", nat_section, "nat-rules"]
        )
        items = self.list_all(
            url=url, aspects=aspects, context="NatGroup.list"
        )
        rtnval = [NatRule.from_dict(item) for item in items]
        return rtnval

    def get(
        self,
        *,
        gateway_id: str,
        rule_id: str,
        nat_section: str = _USER_NAT,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> NatRule:
        """
            Retrieve a single NAT rule by id.

            :param gateway_id: The Tier-1 gateway identifier.
            :param rule_id: The NAT rule identifier.
            :param nat_section: The NAT section id.
            :param aspects: Behaviour controls.

            :returns: A :class:`NatRule`.
        """
        url = self.compose_url(
            parts=[gateway_id, "nat", nat_section, "nat-rules", rule_id]
        )
        body = self.get_json(
            url=url, aspects=aspects, context="NatGroup.get"
        )
        rtnval = NatRule.from_dict(body)
        return rtnval

    def create_or_update(
        self,
        *,
        gateway_id: str,
        rule_id: str,
        spec: NatRuleSpec,
        nat_section: str = _USER_NAT,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> NsxRealizationHandle:
        """
            Create or update a NAT rule (policy upsert via PATCH).

            :param gateway_id: The Tier-1 gateway identifier.
            :param rule_id: The NAT rule identifier.
            :param spec: A :class:`NatRuleSpec`.
            :param nat_section: The NAT section id.
            :param aspects: Behaviour controls.

            :returns: An :class:`NsxRealizationHandle`.
        """
        url = self.compose_url(
            parts=[gateway_id, "nat", nat_section, "nat-rules", rule_id]
        )
        self.patch_json(
            url=url,
            body=spec.to_dict(),
            aspects=aspects,
            context="NatGroup.create_or_update",
        )
        intent_path = (
            "/infra/tier-1s/{}/nat/{}/nat-rules/{}".format(
                gateway_id, nat_section, rule_id
            )
        )
        rtnval = NsxRealizationHandle(
            intent_path=intent_path, client=self.client
        )
        return rtnval

    def delete(
        self,
        *,
        gateway_id: str,
        rule_id: str,
        nat_section: str = _USER_NAT,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> None:
        """
            Delete a NAT rule by id.

            :param gateway_id: The Tier-1 gateway identifier.
            :param rule_id: The NAT rule identifier.
            :param nat_section: The NAT section id.
            :param aspects: Behaviour controls.

            :returns: ``None``
        """
        url = self.compose_url(
            parts=[gateway_id, "nat", nat_section, "nat-rules", rule_id]
        )
        self.delete_resource(
            url=url, aspects=aspects, context="NatGroup.delete"
        )
        return None
