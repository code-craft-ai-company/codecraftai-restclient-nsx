"""
    Tests for :class:`NsxClient` construction, URL composition, and
    session-token authentication.
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


import pytest

from automojo.credentials.apitokencredential import ApiTokenCredential
from automojo.errors.exceptions import SemanticError

from automojo.interop.nsx.nsxclient import NsxClient
from automojo.interop.nsx.nsxsession import XSRF_HEADER

from automojo.tests.interop.nsx.nsxtestsupport import (
    NSX_BASE,
    make_credential,
)


def test_construct_with_basic_credential() -> None:
    client = NsxClient(host="nsx.example.com", credential=make_credential())
    assert client.host == "nsx.example.com"
    return


def test_construct_rejects_non_basic_credential() -> None:
    bad = ApiTokenCredential(
        identifier="t", categories=["api-token"], token="x"
    )
    with pytest.raises(SemanticError):
        NsxClient(host="nsx.example.com", credential=bad)
    return


def test_build_url_accepts_policy_leaf() -> None:
    client = NsxClient(host="nsx.example.com", credential=make_credential())
    url = client.build_url(leaf="/policy/api/v1/infra/segments")
    assert url == NSX_BASE + "/policy/api/v1/infra/segments"
    return


def test_build_url_rejects_non_policy_leaf() -> None:
    client = NsxClient(host="nsx.example.com", credential=make_credential())
    with pytest.raises(SemanticError):
        client.build_url(leaf="/api/session/create")
    return


def test_unknown_group_raises_attribute_error() -> None:
    client = NsxClient(host="nsx.example.com", credential=make_credential())
    with pytest.raises(AttributeError):
        _ = client.NoSuchGroup
    return


def test_authenticate_mints_session_token(requests_mock) -> None:
    requests_mock.post(
        NSX_BASE + "/api/session/create",
        headers={XSRF_HEADER: "xsrf-abc"},
        status_code=200,
    )
    client = NsxClient(host="nsx.example.com", credential=make_credential())
    client.authenticate()
    assert client.auth_token == "xsrf-abc"
    assert client._session.headers[XSRF_HEADER] == "xsrf-abc"
    return


def test_ensure_session_authenticates_lazily(requests_mock) -> None:
    requests_mock.post(
        NSX_BASE + "/api/session/create",
        headers={XSRF_HEADER: "xsrf-lazy"},
        status_code=200,
    )
    client = NsxClient(host="nsx.example.com", credential=make_credential())
    session = client.ensure_session(aspects=client.aspects)
    assert session is not None
    assert client.auth_token == "xsrf-lazy"
    return
