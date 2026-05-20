"""
    .. module:: loadbalancersgroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Load balancer API group for :class:`NsxClient`.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import List

from automojo.restclient.nsx.apigroups.basegroup import BaseGroup
from automojo.restclient.nsx.aspectsnsx import AspectsNsx, DEFAULT_NSX_ASPECTS
from automojo.restclient.nsx.model.services import (
    LbPool,
    LbVirtualServer,
    LoadBalancerSummary,
)
from automojo.restclient.nsx.nsxrealizationhandle import NsxRealizationHandle
from automojo.restclient.nsx.specs.servicesspec import (
    LbPoolSpec,
    LbVirtualServerSpec,
    LoadBalancerSpec,
)


class LoadBalancersGroup(BaseGroup):
    """
        Operations on NSX-T load balancer services, virtual servers and
        server pools (``/policy/api/v1/infra/lb-services`` and related
        collections).
    """

    BASE_LEAF = "/policy/api/v1/infra/lb-services"

    # ------------------------------------------------------------------
    # LB services
    # ------------------------------------------------------------------

    def list(
        self,
        *,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> List[LoadBalancerSummary]:
        """
            List every load balancer service.

            :param aspects: Behaviour controls.

            :returns: List of :class:`LoadBalancerSummary`.
        """
        url = self.compose_url()
        items = self.list_all(
            url=url, aspects=aspects, context="LoadBalancersGroup.list"
        )
        rtnval = [LoadBalancerSummary.from_dict(item) for item in items]
        return rtnval

    def get(
        self,
        *,
        lb_id: str,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> LoadBalancerSummary:
        """
            Retrieve a single load balancer service by id.

            :param lb_id: The load balancer service identifier.
            :param aspects: Behaviour controls.

            :returns: A :class:`LoadBalancerSummary`.
        """
        url = self.compose_url(parts=[lb_id])
        body = self.get_json(
            url=url, aspects=aspects, context="LoadBalancersGroup.get"
        )
        rtnval = LoadBalancerSummary.from_dict(body)
        return rtnval

    def create_or_update(
        self,
        *,
        lb_id: str,
        spec: LoadBalancerSpec,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> NsxRealizationHandle:
        """
            Create or update a load balancer service (upsert via
            PATCH).

            :param lb_id: The load balancer service identifier.
            :param spec: A :class:`LoadBalancerSpec`.
            :param aspects: Behaviour controls.

            :returns: An :class:`NsxRealizationHandle`.
        """
        url = self.compose_url(parts=[lb_id])
        self.patch_json(
            url=url,
            body=spec.to_dict(),
            aspects=aspects,
            context="LoadBalancersGroup.create_or_update",
        )
        intent_path = "/infra/lb-services/{}".format(lb_id)
        rtnval = NsxRealizationHandle(
            intent_path=intent_path, client=self.client
        )
        return rtnval

    def delete(
        self,
        *,
        lb_id: str,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> None:
        """
            Delete a load balancer service by id.

            :param lb_id: The load balancer service identifier.
            :param aspects: Behaviour controls.

            :returns: ``None``
        """
        url = self.compose_url(parts=[lb_id])
        self.delete_resource(
            url=url, aspects=aspects, context="LoadBalancersGroup.delete"
        )
        return None

    # ------------------------------------------------------------------
    # Virtual servers
    # ------------------------------------------------------------------

    def list_virtual_servers(
        self,
        *,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> List[LbVirtualServer]:
        """
            List every load balancer virtual server.

            :param aspects: Behaviour controls.

            :returns: List of :class:`LbVirtualServer`.
        """
        url = self.client.build_url(
            leaf="/policy/api/v1/infra/lb-virtual-servers"
        )
        items = self.list_all(
            url=url,
            aspects=aspects,
            context="LoadBalancersGroup.list_virtual_servers",
        )
        rtnval = [LbVirtualServer.from_dict(item) for item in items]
        return rtnval

    def create_or_update_virtual_server(
        self,
        *,
        virtual_server_id: str,
        spec: LbVirtualServerSpec,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> NsxRealizationHandle:
        """
            Create or update a load balancer virtual server (upsert via
            PATCH).

            :param virtual_server_id: The virtual server identifier.
            :param spec: A :class:`LbVirtualServerSpec`.
            :param aspects: Behaviour controls.

            :returns: An :class:`NsxRealizationHandle`.
        """
        leaf = "/policy/api/v1/infra/lb-virtual-servers/{}".format(
            virtual_server_id
        )
        url = self.client.build_url(leaf=leaf)
        self.patch_json(
            url=url,
            body=spec.to_dict(),
            aspects=aspects,
            context="LoadBalancersGroup.create_or_update_virtual_server",
        )
        intent_path = "/infra/lb-virtual-servers/{}".format(
            virtual_server_id
        )
        rtnval = NsxRealizationHandle(
            intent_path=intent_path, client=self.client
        )
        return rtnval

    # ------------------------------------------------------------------
    # Server pools
    # ------------------------------------------------------------------

    def list_pools(
        self,
        *,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> List[LbPool]:
        """
            List every load balancer server pool.

            :param aspects: Behaviour controls.

            :returns: List of :class:`LbPool`.
        """
        url = self.client.build_url(leaf="/policy/api/v1/infra/lb-pools")
        items = self.list_all(
            url=url,
            aspects=aspects,
            context="LoadBalancersGroup.list_pools",
        )
        rtnval = [LbPool.from_dict(item) for item in items]
        return rtnval

    def create_or_update_pool(
        self,
        *,
        pool_id: str,
        spec: LbPoolSpec,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> NsxRealizationHandle:
        """
            Create or update a load balancer server pool (upsert via
            PATCH).

            :param pool_id: The server pool identifier.
            :param spec: A :class:`LbPoolSpec`.
            :param aspects: Behaviour controls.

            :returns: An :class:`NsxRealizationHandle`.
        """
        leaf = "/policy/api/v1/infra/lb-pools/{}".format(pool_id)
        url = self.client.build_url(leaf=leaf)
        self.patch_json(
            url=url,
            body=spec.to_dict(),
            aspects=aspects,
            context="LoadBalancersGroup.create_or_update_pool",
        )
        intent_path = "/infra/lb-pools/{}".format(pool_id)
        rtnval = NsxRealizationHandle(
            intent_path=intent_path, client=self.client
        )
        return rtnval
