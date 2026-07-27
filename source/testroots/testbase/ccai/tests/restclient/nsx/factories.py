"""
    .. module:: factories
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Test resource factories for the NSX client tests.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from collections.abc import Generator

import requests_mock as requests_mock_module

from ccai import testbase


@testbase.register.resource_factory()
def create_nsx_requests_mock(
        constraints=None) -> Generator[requests_mock_module.Mocker, None, None]:
    """
        Yield an active ``requests_mock`` Mocker for one test.

        Stands in for the ``requests_mock`` pytest plugin fixture, which
        testbase cannot supply — the tests asked for it by name and errored as
        an unresolvable parameter, so none of them ran.

        Attached per test rather than originated in this scope: a Mocker
        accumulates the URIs registered against it, so a shared one would let
        one test's registrations answer another test's requests.

        :param constraints: Optional constraint dictionary.

        :returns: A generator yielding an active Mocker, deactivated afterwards.
    """
    with requests_mock_module.Mocker() as mocker:
        yield mocker
