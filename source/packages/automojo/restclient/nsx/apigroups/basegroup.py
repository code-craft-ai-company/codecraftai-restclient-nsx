"""
    .. module:: basegroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Shared base class for every NSX-T ``*Group`` API surface.
        Adds Policy-API URL composition and cursor-paging helpers on top
        of the generic :class:`RestApiGroup`.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


import os

from http import HTTPStatus
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from automojo.errors.exceptions import SemanticError
from automojo.errors.raising import raise_for_http_status
from automojo.restclient.base.restapigroup import RestApiGroup


if TYPE_CHECKING:
    from automojo.restclient.nsx.aspectsnsx import AspectsNsx
    from automojo.restclient.nsx.nsxclient import NsxClient


_POLICY_PREFIX = "/policy/api/v1/"


class BaseGroup(RestApiGroup):
    """
        Common ancestor for every NSX-T Policy API group.

        Subclasses MUST set :data:`BASE_LEAF` to a value that begins
        with ``/policy/api/v1/`` so the client knows it is composing
        against the Policy API root.  The prefix is validated at
        subclass-registration time so misconfiguration fails fast.
    """

    BASE_LEAF: str = ""

    def __init_subclass__(cls, **kwargs) -> None:
        """
            Validate ``BASE_LEAF`` of subclasses at class-definition
            time.

            :returns: ``None``

            :raises: SemanticError
        """
        super().__init_subclass__(**kwargs)
        if cls is BaseGroup:
            return None

        base = cls.BASE_LEAF
        if base is None or len(base) == 0:
            err_msg_lines = [
                "NSX API group must declare a non-empty BASE_LEAF.",
                "CLASS: {}".format(cls.__name__),
            ]
            err_msg = os.linesep.join(err_msg_lines)
            raise SemanticError(err_msg)

        if not base.startswith(_POLICY_PREFIX):
            err_msg_lines = [
                "NSX API group BASE_LEAF must begin with "
                "'/policy/api/v1/'.",
                "CLASS: {}".format(cls.__name__),
                "GOT: {!r}".format(base),
            ]
            err_msg = os.linesep.join(err_msg_lines)
            raise SemanticError(err_msg)

        return None

    def __init__(self, client: "NsxClient") -> None:
        """
            Initialise the group with a back-reference to the client.

            :param client: Owning :class:`NsxClient` instance.

            :returns: ``None``
        """
        super().__init__(client)
        return

    # ------------------------------------------------------------------
    # URL composition
    # ------------------------------------------------------------------

    def compose_url(self, *, parts: Optional[List[str]] = None) -> str:
        """
            Compose an absolute URL by joining BASE_LEAF with any
            additional path parts.

            :param parts: Optional list of additional path segments
                appended after BASE_LEAF.

            :returns: The absolute URL composed against the client.
        """
        client = self.client
        if parts is None or len(parts) == 0:
            leaf = self.BASE_LEAF
        else:
            leaf = self.build_leaf(parts=parts)
            if not leaf.startswith("/"):
                leaf = "/" + leaf

        rtnval = client.build_url(leaf=leaf)
        return rtnval

    # ------------------------------------------------------------------
    # HTTP helpers
    # ------------------------------------------------------------------

    def get_json(
        self,
        *,
        url: str,
        aspects: "AspectsNsx",
        params: Optional[Dict[str, Any]] = None,
        context: str,
    ) -> Any:
        """
            Issue a GET, validate the status, and return the parsed
            JSON body.

            :param url: Fully-qualified request URL.
            :param aspects: Behaviour controls.
            :param params: Optional query parameters.
            :param context: Context string used in error reporting.

            :returns: The parsed JSON body.
        """
        client = self.client
        session = client.ensure_session(aspects=aspects)
        resp = session.get(
            url,
            params=params,
            timeout=aspects.completion_timeout,
        )
        if resp.status_code != HTTPStatus.OK:
            raise_for_http_status(
                resp.status_code, resp.content, url, context=context
            )
        rtnval = resp.json()
        return rtnval

    def patch_json(
        self,
        *,
        url: str,
        body: Dict[str, Any],
        aspects: "AspectsNsx",
        context: str,
    ) -> Any:
        """
            Issue a PATCH (the NSX-T policy upsert verb), validate the
            status, and return the parsed JSON body.

            :param url: Fully-qualified request URL.
            :param body: Request body dictionary.
            :param aspects: Behaviour controls.
            :param context: Context string used in error reporting.

            :returns: The parsed JSON body, or ``None`` when the manager
                returns an empty body.
        """
        client = self.client
        session = client.ensure_session(aspects=aspects)
        resp = session.patch(
            url,
            json=body,
            timeout=aspects.completion_timeout,
        )
        if resp.status_code not in (HTTPStatus.OK, HTTPStatus.CREATED):
            raise_for_http_status(
                resp.status_code, resp.content, url, context=context
            )
        rtnval: Any = None
        content = resp.content
        if content is not None and len(content) > 0:
            rtnval = resp.json()
        return rtnval

    def delete_resource(
        self,
        *,
        url: str,
        aspects: "AspectsNsx",
        context: str,
    ) -> None:
        """
            Issue a DELETE and validate the status.

            :param url: Fully-qualified request URL.
            :param aspects: Behaviour controls.
            :param context: Context string used in error reporting.

            :returns: ``None``
        """
        client = self.client
        session = client.ensure_session(aspects=aspects)
        resp = session.delete(url, timeout=aspects.completion_timeout)
        if resp.status_code not in (HTTPStatus.OK, HTTPStatus.NO_CONTENT):
            raise_for_http_status(
                resp.status_code, resp.content, url, context=context
            )
        return None

    # ------------------------------------------------------------------
    # Cursor paging
    # ------------------------------------------------------------------

    def list_all(
        self,
        *,
        url: str,
        aspects: "AspectsNsx",
        context: str,
        page_size: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
            Enumerate every item of an NSX-T Policy list endpoint,
            following the ``cursor`` token across pages.

            NSX-T Policy list responses carry a ``results`` array and an
            optional ``cursor`` string.  When the ``cursor`` is absent
            the final page has been reached.

            :param url: Fully-qualified list-endpoint URL.
            :param aspects: Behaviour controls.
            :param context: Context string used in error reporting.
            :param page_size: Optional ``page_size`` query parameter.

            :returns: The accumulated list of result dictionaries.
        """
        rtnval: List[Dict[str, Any]] = []
        cursor: Optional[str] = None

        while True:
            params: Dict[str, Any] = {}
            if page_size is not None:
                params["page_size"] = page_size
            if cursor is not None:
                params["cursor"] = cursor

            page = self.get_json(
                url=url,
                aspects=aspects,
                params=params,
                context=context,
            )

            results = page.get("results")
            if results is None:
                err_msg_lines = [
                    "NSX-T list response missing 'results' field.",
                    "CONTEXT: {}".format(context),
                    "URL: {}".format(url),
                ]
                err_msg = os.linesep.join(err_msg_lines)
                raise SemanticError(err_msg)

            for item in results:
                rtnval.append(item)

            cursor = page.get("cursor")
            if cursor is None:
                break

        return rtnval
