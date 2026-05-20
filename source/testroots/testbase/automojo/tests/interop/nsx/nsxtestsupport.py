"""
    Shared helpers for NSX-T interop client tests.
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from automojo.credentials.basiccredential import BasicCredential

from automojo.interop.nsx.nsxclient import NsxClient


NSX_HOST = "nsx.example.com"
NSX_BASE = "https://nsx.example.com"


def make_credential() -> BasicCredential:
    """
        Build a throwaway :class:`BasicCredential` for client tests.

        :returns: A :class:`BasicCredential`.
    """
    rtnval = BasicCredential(
        identifier="nsx",
        categories=["basic"],
        username="admin",
        password="secret",
    )
    return rtnval


def make_authenticated_client() -> NsxClient:
    """
        Build an :class:`NsxClient` with a pre-installed fake session so
        ``ensure_session`` does not attempt a real auth round-trip.

        The ``requests-mock`` adapter is mounted on the session by the
        caller-supplied ``requests_mock`` fixture; here we only need a
        client whose ``_session`` is non-``None``.

        :returns: An :class:`NsxClient` ready for mocked calls.
    """
    import requests

    cred = make_credential()
    client = NsxClient(host=NSX_HOST, credential=cred)
    client._session = requests.Session()
    client._auth_token = "xsrf-token-1"
    return client
