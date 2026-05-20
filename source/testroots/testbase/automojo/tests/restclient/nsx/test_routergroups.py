"""
    Behavioural tests for :class:`T0RoutersGroup` and
    :class:`T1RoutersGroup` with fully mocked HTTP.
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from automojo.restclient.nsx.model.gateway import (
    T0GatewaySummary,
    T1GatewaySummary,
)
from automojo.restclient.nsx.nsxrealizationhandle import NsxRealizationHandle
from automojo.restclient.nsx.specs.gatewayspec import T0GatewaySpec, T1GatewaySpec

from automojo.tests.restclient.nsx.nsxtestsupport import (
    NSX_BASE,
    make_authenticated_client,
)


_T0_URL = NSX_BASE + "/policy/api/v1/infra/tier-0s"
_T1_URL = NSX_BASE + "/policy/api/v1/infra/tier-1s"


def test_t0_list(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.get(
        _T0_URL,
        json={"results": [{"id": "t0-a", "display_name": "T0 A"}]},
    )
    result = client.T0Routers.list()
    assert len(result) == 1
    assert isinstance(result[0], T0GatewaySummary)
    return


def test_t0_get(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.get(
        _T0_URL + "/t0-a",
        json={"id": "t0-a", "display_name": "T0 A", "ha_mode": "ACTIVE_STANDBY"},
    )
    result = client.T0Routers.get(gateway_id="t0-a")
    assert result.ha_mode == "ACTIVE_STANDBY"
    return


def test_t0_create_or_update(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.patch(_T0_URL + "/t0-new", json={"id": "t0-new"})
    spec = T0GatewaySpec(display_name="Edge", ha_mode="ACTIVE_ACTIVE")
    handle = client.T0Routers.create_or_update(
        gateway_id="t0-new", spec=spec
    )
    assert isinstance(handle, NsxRealizationHandle)
    assert handle.task_id() == "/infra/tier-0s/t0-new"
    return


def test_t0_delete(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.delete(_T0_URL + "/t0-old", status_code=204)
    client.T0Routers.delete(gateway_id="t0-old")
    assert requests_mock.request_history[0].method == "DELETE"
    return


def test_t1_list(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.get(
        _T1_URL,
        json={"results": [{"id": "t1-a", "display_name": "T1 A"}]},
    )
    result = client.T1Routers.list()
    assert isinstance(result[0], T1GatewaySummary)
    return


def test_t1_get(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.get(
        _T1_URL + "/t1-a",
        json={"id": "t1-a", "display_name": "T1 A", "tier0_path": "/infra/tier-0s/t0-a"},
    )
    result = client.T1Routers.get(gateway_id="t1-a")
    assert result.tier0_path == "/infra/tier-0s/t0-a"
    return


def test_t1_create_or_update(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.patch(_T1_URL + "/t1-new", json={"id": "t1-new"})
    spec = T1GatewaySpec(
        display_name="Tenant", tier0_path="/infra/tier-0s/t0-a"
    )
    handle = client.T1Routers.create_or_update(
        gateway_id="t1-new", spec=spec
    )
    assert handle.task_id() == "/infra/tier-1s/t1-new"
    body = requests_mock.request_history[0].json()
    assert body["tier0_path"] == "/infra/tier-0s/t0-a"
    return


def test_t1_delete(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.delete(_T1_URL + "/t1-old", status_code=200)
    client.T1Routers.delete(gateway_id="t1-old")
    assert requests_mock.request_history[0].method == "DELETE"
    return
