"""
    .. module:: t0routersgroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tier-0 gateway API group for :class:`NsxClient`.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import List

from ccai.restclient.nsx.apigroups.basegroup import BaseGroup
from ccai.restclient.nsx.aspectsnsx import AspectsNsx, DEFAULT_NSX_ASPECTS
from ccai.restclient.nsx.model.gateway import T0GatewaySummary
from ccai.restclient.nsx.nsxrealizationhandle import NsxRealizationHandle
from ccai.restclient.nsx.specs.gatewayspec import T0GatewaySpec


class T0RoutersGroup(BaseGroup):
    """
        Operations on NSX-T Tier-0 gateways
        (``/policy/api/v1/infra/tier-0s``).
    """

    BASE_LEAF = "/policy/api/v1/infra/tier-0s"

    def list(
        self,
        *,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> List[T0GatewaySummary]:
        """
            List every Tier-0 gateway defined under ``/infra``.

            :param aspects: Behaviour controls.

            :returns: List of :class:`T0GatewaySummary`.
        """
        url = self.compose_url()
        items = self.list_all(
            url=url, aspects=aspects, context="T0RoutersGroup.list"
        )
        rtnval = [T0GatewaySummary.from_dict(item) for item in items]
        return rtnval

    def get(
        self,
        *,
        gateway_id: str,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> T0GatewaySummary:
        """
            Retrieve a single Tier-0 gateway by id.

            :param gateway_id: The Tier-0 gateway identifier.
            :param aspects: Behaviour controls.

            :returns: A :class:`T0GatewaySummary`.
        """
        url = self.compose_url(parts=[gateway_id])
        body = self.get_json(
            url=url, aspects=aspects, context="T0RoutersGroup.get"
        )
        rtnval = T0GatewaySummary.from_dict(body)
        return rtnval

    def create_or_update(
        self,
        *,
        gateway_id: str,
        spec: T0GatewaySpec,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> NsxRealizationHandle:
        """
            Create or update a Tier-0 gateway (policy upsert via PATCH).

            :param gateway_id: The Tier-0 gateway identifier.
            :param spec: A :class:`T0GatewaySpec`.
            :param aspects: Behaviour controls.

            :returns: An :class:`NsxRealizationHandle`.
        """
        url = self.compose_url(parts=[gateway_id])
        self.patch_json(
            url=url,
            body=spec.to_dict(),
            aspects=aspects,
            context="T0RoutersGroup.create_or_update",
        )
        intent_path = "/infra/tier-0s/{}".format(gateway_id)
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
            Delete a Tier-0 gateway by id.

            :param gateway_id: The Tier-0 gateway identifier.
            :param aspects: Behaviour controls.

            :returns: ``None``
        """
        url = self.compose_url(parts=[gateway_id])
        self.delete_resource(
            url=url, aspects=aspects, context="T0RoutersGroup.delete"
        )
        return None
