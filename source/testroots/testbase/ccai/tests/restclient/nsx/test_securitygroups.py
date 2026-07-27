"""
    Behavioural tests for :class:`SecurityGroupsGroup` and
    :class:`DfwGroup` with fully mocked HTTP.
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from ccai.restclient.nsx.model.security import (
    DfwPolicy,
    DfwRule,
    SecurityGroupSummary,
)
from ccai.restclient.nsx.nsxrealizationhandle import NsxRealizationHandle
from ccai.restclient.nsx.specs.securityspec import (
    DfwPolicySpec,
    DfwRuleSpec,
    SecurityGroupSpec,
)

from ccai.tests.restclient.nsx.nsxtestsupport import (
    NSX_BASE,
    make_authenticated_client,
)

from ccai import testbase
from ccai.tests.restclient.nsx.factories import create_nsx_requests_mock


_DOMAIN_BASE = NSX_BASE + "/policy/api/v1/infra/domains/default"
_GROUPS_URL = _DOMAIN_BASE + "/groups"
_POLICIES_URL = _DOMAIN_BASE + "/security-policies"


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_security_group_list(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.get(
        _GROUPS_URL,
        json={"results": [{"id": "g-a", "display_name": "Web"}]},
    )
    result = client.SecurityGroups.list()
    assert isinstance(result[0], SecurityGroupSummary)
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_security_group_get(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.get(
        _GROUPS_URL + "/g-a",
        json={"id": "g-a", "display_name": "Web"},
    )
    result = client.SecurityGroups.get(group_id="g-a")
    assert result.id == "g-a"
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_security_group_create_or_update(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.patch(_GROUPS_URL + "/g-new", json={"id": "g-new"})
    spec = SecurityGroupSpec(
        display_name="DB",
        expression=[{"resource_type": "Condition"}],
    )
    handle = client.SecurityGroups.create_or_update(
        group_id="g-new", spec=spec
    )
    assert isinstance(handle, NsxRealizationHandle)
    assert handle.task_id() == "/infra/domains/default/groups/g-new"
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_security_group_delete(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.delete(_GROUPS_URL + "/g-old", status_code=200)
    client.SecurityGroups.delete(group_id="g-old")
    assert requests_mock.request_history[0].method == "DELETE"
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_dfw_list_policies(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.get(
        _POLICIES_URL,
        json={"results": [{"id": "p-a", "display_name": "App"}]},
    )
    result = client.Dfw.list_policies()
    assert isinstance(result[0], DfwPolicy)
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_dfw_get_policy(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.get(
        _POLICIES_URL + "/p-a",
        json={"id": "p-a", "display_name": "App", "category": "Application"},
    )
    result = client.Dfw.get_policy(policy_id="p-a")
    assert result.category == "Application"
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_dfw_create_policy(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.patch(_POLICIES_URL + "/p-new", json={"id": "p-new"})
    spec = DfwPolicySpec(display_name="App", category="Application")
    handle = client.Dfw.create_or_update_policy(
        policy_id="p-new", spec=spec
    )
    assert handle.task_id() == (
        "/infra/domains/default/security-policies/p-new"
    )
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_dfw_delete_policy(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.delete(_POLICIES_URL + "/p-old", status_code=200)
    client.Dfw.delete_policy(policy_id="p-old")
    assert requests_mock.request_history[0].method == "DELETE"
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_dfw_list_rules(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.get(
        _POLICIES_URL + "/p-a/rules",
        json={"results": [{"id": "r-1", "display_name": "Allow Web"}]},
    )
    result = client.Dfw.list_rules(policy_id="p-a")
    assert isinstance(result[0], DfwRule)
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_dfw_create_rule(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.patch(
        _POLICIES_URL + "/p-a/rules/r-new", json={"id": "r-new"}
    )
    spec = DfwRuleSpec(
        display_name="Allow Web",
        action="ALLOW",
        source_groups=["ANY"],
        services=["/infra/services/HTTP"],
    )
    handle = client.Dfw.create_or_update_rule(
        policy_id="p-a", rule_id="r-new", spec=spec
    )
    assert handle.task_id() == (
        "/infra/domains/default/security-policies/p-a/rules/r-new"
    )
    body = requests_mock.request_history[0].json()
    assert body["action"] == "ALLOW"
    return


@testbase.attach.parameter(create_nsx_requests_mock, identifier="requests_mock")
def test_dfw_delete_rule(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.delete(
        _POLICIES_URL + "/p-a/rules/r-old", status_code=200
    )
    client.Dfw.delete_rule(policy_id="p-a", rule_id="r-old")
    assert requests_mock.request_history[0].method == "DELETE"
    return
