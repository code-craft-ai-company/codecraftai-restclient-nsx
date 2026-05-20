"""
    Round-trip tests for NSX-T DTOs and request specs.
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from automojo.restclient.nsx.model.gateway import (
    T0GatewaySummary,
    T1GatewaySummary,
)
from automojo.restclient.nsx.model.realization import RealizationStateInfo
from automojo.restclient.nsx.model.security import (
    DfwPolicy,
    DfwRule,
    SecurityGroupSummary,
)
from automojo.restclient.nsx.model.segment import SegmentInfo, SegmentSummary
from automojo.restclient.nsx.model.services import (
    LbPool,
    LbVirtualServer,
    LoadBalancerSummary,
    NatRule,
)
from automojo.restclient.nsx.specs.gatewayspec import T0GatewaySpec, T1GatewaySpec
from automojo.restclient.nsx.specs.securityspec import (
    DfwPolicySpec,
    DfwRuleSpec,
    SecurityGroupSpec,
)
from automojo.restclient.nsx.specs.segmentspec import SegmentSpec
from automojo.restclient.nsx.specs.servicesspec import (
    LbPoolSpec,
    LbVirtualServerSpec,
    LoadBalancerSpec,
    NatRuleSpec,
)


def test_segment_summary_roundtrip() -> None:
    data = {"id": "seg-a", "display_name": "S", "vlan_ids": [10]}
    obj = SegmentSummary.from_dict(data)
    assert obj.id == "seg-a"
    assert obj.to_dict()["vlan_ids"] == [10]
    return


def test_segment_info_roundtrip() -> None:
    data = {
        "id": "seg-a",
        "display_name": "S",
        "subnets": [{"gateway_address": "10.0.0.1/24"}],
    }
    obj = SegmentInfo.from_dict(data)
    assert obj.subnets[0]["gateway_address"] == "10.0.0.1/24"
    return


def test_gateway_summaries_roundtrip() -> None:
    t0 = T0GatewaySummary.from_dict(
        {"id": "t0", "display_name": "T0", "ha_mode": "ACTIVE_ACTIVE"}
    )
    t1 = T1GatewaySummary.from_dict(
        {"id": "t1", "display_name": "T1", "tier0_path": "/infra/tier-0s/t0"}
    )
    assert t0.ha_mode == "ACTIVE_ACTIVE"
    assert t1.tier0_path == "/infra/tier-0s/t0"
    return


def test_security_dtos_roundtrip() -> None:
    grp = SecurityGroupSummary.from_dict(
        {"id": "g", "display_name": "G"}
    )
    rule = DfwRule.from_dict(
        {"id": "r", "display_name": "R", "action": "DROP"}
    )
    policy = DfwPolicy.from_dict(
        {"id": "p", "display_name": "P", "category": "Application"}
    )
    assert grp.id == "g"
    assert rule.action == "DROP"
    assert policy.category == "Application"
    return


def test_services_dtos_roundtrip() -> None:
    nat = NatRule.from_dict(
        {"id": "n", "display_name": "N", "action": "SNAT"}
    )
    lb = LoadBalancerSummary.from_dict(
        {"id": "lb", "display_name": "LB", "size": "SMALL"}
    )
    vs = LbVirtualServer.from_dict(
        {"id": "vs", "display_name": "VS", "ports": ["443"]}
    )
    pool = LbPool.from_dict(
        {"id": "pool", "display_name": "Pool", "algorithm": "ROUND_ROBIN"}
    )
    assert nat.action == "SNAT"
    assert lb.size == "SMALL"
    assert vs.ports == ["443"]
    assert pool.algorithm == "ROUND_ROBIN"
    return


def test_realization_info_roundtrip() -> None:
    info = RealizationStateInfo.from_dict(
        {"state": "REALIZED", "publish_status": "REALIZED"}
    )
    assert info.state == "REALIZED"
    return


def test_segment_spec_to_dict_omits_none() -> None:
    spec = SegmentSpec(display_name="S")
    body = spec.to_dict()
    assert body == {"display_name": "S"}
    return


def test_gateway_specs_to_dict() -> None:
    t0 = T0GatewaySpec(display_name="T0", ha_mode="ACTIVE_STANDBY")
    t1 = T1GatewaySpec(display_name="T1", tier0_path="/infra/tier-0s/t0")
    assert t0.to_dict()["ha_mode"] == "ACTIVE_STANDBY"
    assert t1.to_dict()["tier0_path"] == "/infra/tier-0s/t0"
    return


def test_security_specs_to_dict() -> None:
    grp = SecurityGroupSpec(display_name="G")
    rule = DfwRuleSpec(display_name="R", action="REJECT")
    policy = DfwPolicySpec(display_name="P")
    assert grp.to_dict() == {"display_name": "G"}
    assert rule.to_dict()["action"] == "REJECT"
    assert policy.to_dict()["category"] == "Application"
    return


def test_services_specs_to_dict() -> None:
    nat = NatRuleSpec(display_name="N", action="DNAT")
    lb = LoadBalancerSpec(display_name="LB")
    vs = LbVirtualServerSpec(
        display_name="VS", ip_address="1.2.3.4", ports=["80"]
    )
    pool = LbPoolSpec(display_name="Pool")
    assert nat.to_dict()["action"] == "DNAT"
    assert lb.to_dict()["size"] == "SMALL"
    assert vs.to_dict()["ip_address"] == "1.2.3.4"
    assert pool.to_dict()["algorithm"] == "ROUND_ROBIN"
    return
