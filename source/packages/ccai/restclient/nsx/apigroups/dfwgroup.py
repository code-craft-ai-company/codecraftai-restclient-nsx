"""
    .. module:: dfwgroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Distributed-firewall API group for :class:`NsxClient`.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import List

from ccai.restclient.nsx.apigroups.basegroup import BaseGroup
from ccai.restclient.nsx.aspectsnsx import AspectsNsx, DEFAULT_NSX_ASPECTS
from ccai.restclient.nsx.model.security import DfwPolicy, DfwRule
from ccai.restclient.nsx.nsxrealizationhandle import NsxRealizationHandle
from ccai.restclient.nsx.specs.securityspec import DfwPolicySpec, DfwRuleSpec


_DEFAULT_DOMAIN = "default"


class DfwGroup(BaseGroup):
    """
        Operations on the NSX-T distributed firewall: security policies
        and their rules
        (``/policy/api/v1/infra/domains/default/security-policies``).
    """

    BASE_LEAF = "/policy/api/v1/infra/domains"

    # ------------------------------------------------------------------
    # Security policies
    # ------------------------------------------------------------------

    def list_policies(
        self,
        *,
        domain: str = _DEFAULT_DOMAIN,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> List[DfwPolicy]:
        """
            List every DFW security policy within a domain.

            :param domain: The policy domain id.
            :param aspects: Behaviour controls.

            :returns: List of :class:`DfwPolicy`.
        """
        url = self.compose_url(parts=[domain, "security-policies"])
        items = self.list_all(
            url=url, aspects=aspects, context="DfwGroup.list_policies"
        )
        rtnval = [DfwPolicy.from_dict(item) for item in items]
        return rtnval

    def get_policy(
        self,
        *,
        policy_id: str,
        domain: str = _DEFAULT_DOMAIN,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> DfwPolicy:
        """
            Retrieve a single DFW security policy by id.

            :param policy_id: The security policy identifier.
            :param domain: The policy domain id.
            :param aspects: Behaviour controls.

            :returns: A :class:`DfwPolicy`.
        """
        url = self.compose_url(
            parts=[domain, "security-policies", policy_id]
        )
        body = self.get_json(
            url=url, aspects=aspects, context="DfwGroup.get_policy"
        )
        rtnval = DfwPolicy.from_dict(body)
        return rtnval

    def create_or_update_policy(
        self,
        *,
        policy_id: str,
        spec: DfwPolicySpec,
        domain: str = _DEFAULT_DOMAIN,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> NsxRealizationHandle:
        """
            Create or update a DFW security policy (upsert via PATCH).

            :param policy_id: The security policy identifier.
            :param spec: A :class:`DfwPolicySpec`.
            :param domain: The policy domain id.
            :param aspects: Behaviour controls.

            :returns: An :class:`NsxRealizationHandle`.
        """
        url = self.compose_url(
            parts=[domain, "security-policies", policy_id]
        )
        self.patch_json(
            url=url,
            body=spec.to_dict(),
            aspects=aspects,
            context="DfwGroup.create_or_update_policy",
        )
        intent_path = "/infra/domains/{}/security-policies/{}".format(
            domain, policy_id
        )
        rtnval = NsxRealizationHandle(
            intent_path=intent_path, client=self.client
        )
        return rtnval

    def delete_policy(
        self,
        *,
        policy_id: str,
        domain: str = _DEFAULT_DOMAIN,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> None:
        """
            Delete a DFW security policy by id.

            :param policy_id: The security policy identifier.
            :param domain: The policy domain id.
            :param aspects: Behaviour controls.

            :returns: ``None``
        """
        url = self.compose_url(
            parts=[domain, "security-policies", policy_id]
        )
        self.delete_resource(
            url=url, aspects=aspects, context="DfwGroup.delete_policy"
        )
        return None

    # ------------------------------------------------------------------
    # Rules
    # ------------------------------------------------------------------

    def list_rules(
        self,
        *,
        policy_id: str,
        domain: str = _DEFAULT_DOMAIN,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> List[DfwRule]:
        """
            List every rule within a DFW security policy.

            :param policy_id: The security policy identifier.
            :param domain: The policy domain id.
            :param aspects: Behaviour controls.

            :returns: List of :class:`DfwRule`.
        """
        url = self.compose_url(
            parts=[domain, "security-policies", policy_id, "rules"]
        )
        items = self.list_all(
            url=url, aspects=aspects, context="DfwGroup.list_rules"
        )
        rtnval = [DfwRule.from_dict(item) for item in items]
        return rtnval

    def create_or_update_rule(
        self,
        *,
        policy_id: str,
        rule_id: str,
        spec: DfwRuleSpec,
        domain: str = _DEFAULT_DOMAIN,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> NsxRealizationHandle:
        """
            Create or update a DFW rule (policy upsert via PATCH).

            :param policy_id: The owning security policy identifier.
            :param rule_id: The rule identifier.
            :param spec: A :class:`DfwRuleSpec`.
            :param domain: The policy domain id.
            :param aspects: Behaviour controls.

            :returns: An :class:`NsxRealizationHandle`.
        """
        url = self.compose_url(
            parts=[
                domain, "security-policies", policy_id, "rules", rule_id
            ]
        )
        self.patch_json(
            url=url,
            body=spec.to_dict(),
            aspects=aspects,
            context="DfwGroup.create_or_update_rule",
        )
        intent_path = (
            "/infra/domains/{}/security-policies/{}/rules/{}".format(
                domain, policy_id, rule_id
            )
        )
        rtnval = NsxRealizationHandle(
            intent_path=intent_path, client=self.client
        )
        return rtnval

    def delete_rule(
        self,
        *,
        policy_id: str,
        rule_id: str,
        domain: str = _DEFAULT_DOMAIN,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> None:
        """
            Delete a DFW rule by id.

            :param policy_id: The owning security policy identifier.
            :param rule_id: The rule identifier.
            :param domain: The policy domain id.
            :param aspects: Behaviour controls.

            :returns: ``None``
        """
        url = self.compose_url(
            parts=[
                domain, "security-policies", policy_id, "rules", rule_id
            ]
        )
        self.delete_resource(
            url=url, aspects=aspects, context="DfwGroup.delete_rule"
        )
        return None
