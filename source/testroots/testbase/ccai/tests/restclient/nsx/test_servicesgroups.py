"""
    Behavioural tests for :class:`NatGroup` and
    :class:`LoadBalancersGroup` with fully mocked HTTP.
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from ccai.restclient.nsx.model.services import (
    LbPool,
    LbVirtualServer,
    LoadBalancerSummary,
    NatRule,
)
from ccai.restclient.nsx.nsxrealizationhandle import NsxRealizationHandle
from ccai.restclient.nsx.specs.servicesspec import (
    LbPoolSpec,
    LbVirtualServerSpec,
    LoadBalancerSpec,
    NatRuleSpec,
)

from .nsxtestsupport import (
    NSX_BASE,
    make_authenticated_client,
)

from ccai import testbase
from .factories import create_nsx_requests_mock


_NAT_BASE = (
    NSX_BASE + "/policy/api/v1/infra/tier-1s/t1-a/nat/USER/nat-rules"
)
_LB_URL = NSX_BASE + "/policy/api/v1/infra/lb-services"
_VS_URL = NSX_BASE + "/policy/api/v1/infra/lb-virtual-servers"
_POOL_URL = NSX_BASE + "/policy/api/v1/infra/lb-pools"


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_nat_list(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.get(
        _NAT_BASE,
        json={"results": [{"id": "n-1", "display_name": "SNAT"}]},
    )
    result = client.Nat.list(gateway_id="t1-a")
    assert isinstance(result[0], NatRule)
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_nat_get(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.get(
        _NAT_BASE + "/n-1",
        json={"id": "n-1", "display_name": "SNAT", "action": "SNAT"},
    )
    result = client.Nat.get(gateway_id="t1-a", rule_id="n-1")
    assert result.action == "SNAT"
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_nat_create_or_update(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.patch(_NAT_BASE + "/n-new", json={"id": "n-new"})
    spec = NatRuleSpec(
        display_name="SNAT",
        action="SNAT",
        source_network="10.0.0.0/24",
        translated_network="203.0.113.5",
    )
    handle = client.Nat.create_or_update(
        gateway_id="t1-a", rule_id="n-new", spec=spec
    )
    assert isinstance(handle, NsxRealizationHandle)
    assert handle.task_id() == (
        "/infra/tier-1s/t1-a/nat/USER/nat-rules/n-new"
    )
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_nat_delete(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.delete(_NAT_BASE + "/n-old", status_code=200)
    client.Nat.delete(gateway_id="t1-a", rule_id="n-old")
    assert requests_mock.request_history[0].method == "DELETE"
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_lb_list(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.get(
        _LB_URL,
        json={"results": [{"id": "lb-a", "display_name": "Web LB"}]},
    )
    result = client.LoadBalancers.list()
    assert isinstance(result[0], LoadBalancerSummary)
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_lb_get(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.get(
        _LB_URL + "/lb-a",
        json={"id": "lb-a", "display_name": "Web LB", "size": "SMALL"},
    )
    result = client.LoadBalancers.get(lb_id="lb-a")
    assert result.size == "SMALL"
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_lb_create_or_update(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.patch(_LB_URL + "/lb-new", json={"id": "lb-new"})
    spec = LoadBalancerSpec(
        display_name="Web LB",
        connectivity_path="/infra/tier-1s/t1-a",
        size="MEDIUM",
    )
    handle = client.LoadBalancers.create_or_update(
        lb_id="lb-new", spec=spec
    )
    assert handle.task_id() == "/infra/lb-services/lb-new"
    body = requests_mock.request_history[0].json()
    assert body["size"] == "MEDIUM"
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_lb_delete(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.delete(_LB_URL + "/lb-old", status_code=200)
    client.LoadBalancers.delete(lb_id="lb-old")
    assert requests_mock.request_history[0].method == "DELETE"
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_lb_virtual_servers(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.get(
        _VS_URL,
        json={"results": [{"id": "vs-a", "display_name": "VS A"}]},
    )
    result = client.LoadBalancers.list_virtual_servers()
    assert isinstance(result[0], LbVirtualServer)
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_lb_create_virtual_server(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.patch(_VS_URL + "/vs-new", json={"id": "vs-new"})
    spec = LbVirtualServerSpec(
        display_name="VS A",
        ip_address="203.0.113.10",
        ports=["443"],
        pool_path="/infra/lb-pools/pool-a",
    )
    handle = client.LoadBalancers.create_or_update_virtual_server(
        virtual_server_id="vs-new", spec=spec
    )
    assert handle.task_id() == "/infra/lb-virtual-servers/vs-new"
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_lb_pools(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.get(
        _POOL_URL,
        json={"results": [{"id": "pool-a", "display_name": "Pool A"}]},
    )
    result = client.LoadBalancers.list_pools()
    assert isinstance(result[0], LbPool)
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_lb_create_pool(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.patch(_POOL_URL + "/pool-new", json={"id": "pool-new"})
    spec = LbPoolSpec(
        display_name="Pool A",
        algorithm="LEAST_CONNECTION",
        members=[{"ip_address": "10.0.0.5"}],
    )
    handle = client.LoadBalancers.create_or_update_pool(
        pool_id="pool-new", spec=spec
    )
    assert handle.task_id() == "/infra/lb-pools/pool-new"
    return
