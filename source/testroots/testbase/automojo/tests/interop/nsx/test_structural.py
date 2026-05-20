"""
    Structural tests: every NSX API group is registered and inherits
    :class:`RestApiGroup`; every BASE_LEAF targets the Policy API root.
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from automojo.restclient.base.restapigroup import RestApiGroup

from automojo.interop.nsx.apigroups.basegroup import BaseGroup
from automojo.interop.nsx.nsxclient import _GROUP_REGISTRY

from automojo.tests.interop.nsx.nsxtestsupport import make_credential
from automojo.interop.nsx.nsxclient import NsxClient


def test_every_registered_group_resolves() -> None:
    client = NsxClient(host="nsx.example.com", credential=make_credential())
    for entry_name, _module, _cls in _GROUP_REGISTRY:
        group = getattr(client, entry_name)
        assert isinstance(group, RestApiGroup)
        assert isinstance(group, BaseGroup)
    return


def test_every_group_base_leaf_is_policy_rooted() -> None:
    client = NsxClient(host="nsx.example.com", credential=make_credential())
    for entry_name, _module, _cls in _GROUP_REGISTRY:
        group = getattr(client, entry_name)
        assert group.BASE_LEAF.startswith("/policy/api/v1/")
    return


def test_groups_are_cached() -> None:
    client = NsxClient(host="nsx.example.com", credential=make_credential())
    first = client.Segments
    second = client.Segments
    assert first is second
    return


def test_registry_covers_expected_surface() -> None:
    names = {entry[0] for entry in _GROUP_REGISTRY}
    expected = {
        "Segments",
        "T0Routers",
        "T1Routers",
        "SecurityGroups",
        "Dfw",
        "Nat",
        "LoadBalancers",
    }
    assert names == expected
    return
