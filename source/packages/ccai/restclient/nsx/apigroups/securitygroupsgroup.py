"""
    .. module:: securitygroupsgroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Security groups API group for :class:`NsxClient`.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import List

from ccai.restclient.nsx.apigroups.basegroup import BaseGroup
from ccai.restclient.nsx.aspectsnsx import AspectsNsx, DEFAULT_NSX_ASPECTS
from ccai.restclient.nsx.model.security import SecurityGroupSummary
from ccai.restclient.nsx.nsxrealizationhandle import NsxRealizationHandle
from ccai.restclient.nsx.specs.securityspec import SecurityGroupSpec


# NSX-T policy security groups live under a domain; ``default`` is the
# domain present on every manager.
_DEFAULT_DOMAIN = "default"


class SecurityGroupsGroup(BaseGroup):
    """
        Operations on NSX-T policy security groups
        (``/policy/api/v1/infra/domains/default/groups``).
    """

    BASE_LEAF = "/policy/api/v1/infra/domains"

    def _groups_url(self, *, domain: str) -> str:
        """
            Compose the groups collection URL for a domain.

            :param domain: The policy domain id.

            :returns: The absolute collection URL.
        """
        rtnval = self.compose_url(parts=[domain, "groups"])
        return rtnval

    def list(
        self,
        *,
        domain: str = _DEFAULT_DOMAIN,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> List[SecurityGroupSummary]:
        """
            List every security group within a policy domain.

            :param domain: The policy domain id.
            :param aspects: Behaviour controls.

            :returns: List of :class:`SecurityGroupSummary`.
        """
        url = self._groups_url(domain=domain)
        items = self.list_all(
            url=url, aspects=aspects, context="SecurityGroupsGroup.list"
        )
        rtnval = [SecurityGroupSummary.from_dict(item) for item in items]
        return rtnval

    def get(
        self,
        *,
        group_id: str,
        domain: str = _DEFAULT_DOMAIN,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> SecurityGroupSummary:
        """
            Retrieve a single security group by id.

            :param group_id: The group identifier.
            :param domain: The policy domain id.
            :param aspects: Behaviour controls.

            :returns: A :class:`SecurityGroupSummary`.
        """
        url = self.compose_url(parts=[domain, "groups", group_id])
        body = self.get_json(
            url=url, aspects=aspects, context="SecurityGroupsGroup.get"
        )
        rtnval = SecurityGroupSummary.from_dict(body)
        return rtnval

    def create_or_update(
        self,
        *,
        group_id: str,
        spec: SecurityGroupSpec,
        domain: str = _DEFAULT_DOMAIN,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> NsxRealizationHandle:
        """
            Create or update a security group (policy upsert via PATCH).

            :param group_id: The group identifier.
            :param spec: A :class:`SecurityGroupSpec`.
            :param domain: The policy domain id.
            :param aspects: Behaviour controls.

            :returns: An :class:`NsxRealizationHandle`.
        """
        url = self.compose_url(parts=[domain, "groups", group_id])
        self.patch_json(
            url=url,
            body=spec.to_dict(),
            aspects=aspects,
            context="SecurityGroupsGroup.create_or_update",
        )
        intent_path = "/infra/domains/{}/groups/{}".format(domain, group_id)
        rtnval = NsxRealizationHandle(
            intent_path=intent_path, client=self.client
        )
        return rtnval

    def delete(
        self,
        *,
        group_id: str,
        domain: str = _DEFAULT_DOMAIN,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> None:
        """
            Delete a security group by id.

            :param group_id: The group identifier.
            :param domain: The policy domain id.
            :param aspects: Behaviour controls.

            :returns: ``None``
        """
        url = self.compose_url(parts=[domain, "groups", group_id])
        self.delete_resource(
            url=url, aspects=aspects, context="SecurityGroupsGroup.delete"
        )
        return None
