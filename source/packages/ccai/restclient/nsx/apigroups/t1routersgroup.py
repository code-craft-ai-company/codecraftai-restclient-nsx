"""
    .. module:: t1routersgroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tier-1 gateway API group for :class:`NsxClient`.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import List

from ccai.restclient.nsx.apigroups.basegroup import BaseGroup
from ccai.restclient.nsx.aspectsnsx import AspectsNsx, DEFAULT_NSX_ASPECTS
from ccai.restclient.nsx.model.gateway import T1GatewaySummary
from ccai.restclient.nsx.nsxrealizationhandle import NsxRealizationHandle
from ccai.restclient.nsx.specs.gatewayspec import T1GatewaySpec


class T1RoutersGroup(BaseGroup):
    """
        Operations on NSX-T Tier-1 gateways
        (``/policy/api/v1/infra/tier-1s``).
    """

    BASE_LEAF = "/policy/api/v1/infra/tier-1s"

    def list(
        self,
        *,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> List[T1GatewaySummary]:
        """
            List every Tier-1 gateway defined under ``/infra``.

            :param aspects: Behaviour controls.

            :returns: List of :class:`T1GatewaySummary`.
        """
        url = self.compose_url()
        items = self.list_all(
            url=url, aspects=aspects, context="T1RoutersGroup.list"
        )
        rtnval = [T1GatewaySummary.from_dict(item) for item in items]
        return rtnval

    def get(
        self,
        *,
        gateway_id: str,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> T1GatewaySummary:
        """
            Retrieve a single Tier-1 gateway by id.

            :param gateway_id: The Tier-1 gateway identifier.
            :param aspects: Behaviour controls.

            :returns: A :class:`T1GatewaySummary`.
        """
        url = self.compose_url(parts=[gateway_id])
        body = self.get_json(
            url=url, aspects=aspects, context="T1RoutersGroup.get"
        )
        rtnval = T1GatewaySummary.from_dict(body)
        return rtnval

    def create_or_update(
        self,
        *,
        gateway_id: str,
        spec: T1GatewaySpec,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> NsxRealizationHandle:
        """
            Create or update a Tier-1 gateway (policy upsert via PATCH).

            :param gateway_id: The Tier-1 gateway identifier.
            :param spec: A :class:`T1GatewaySpec`.
            :param aspects: Behaviour controls.

            :returns: An :class:`NsxRealizationHandle`.
        """
        url = self.compose_url(parts=[gateway_id])
        self.patch_json(
            url=url,
            body=spec.to_dict(),
            aspects=aspects,
            context="T1RoutersGroup.create_or_update",
        )
        intent_path = "/infra/tier-1s/{}".format(gateway_id)
        rtnval = NsxRealizationHandle(
            intent_path=intent_path, client=self.client
        )
        return rtnval

    def delete(
        self,
        *,
        gateway_id: str,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> None:
        """
            Delete a Tier-1 gateway by id.

            :param gateway_id: The Tier-1 gateway identifier.
            :param aspects: Behaviour controls.

            :returns: ``None``
        """
        url = self.compose_url(parts=[gateway_id])
        self.delete_resource(
            url=url, aspects=aspects, context="T1RoutersGroup.delete"
        )
        return None
