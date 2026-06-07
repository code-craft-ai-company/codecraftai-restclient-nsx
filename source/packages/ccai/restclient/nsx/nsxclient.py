"""
    .. module:: nsxclient
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Provides :class:`NsxClient`, a :class:`RestClientBase`
        subclass that talks to the NSX-T Manager Policy API and exposes
        lazy-cached API group properties.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


import os
import threading

from typing import Any, Dict, Optional

from requests import Session

from ccai.credentials.basecredential import BaseCredential
from ccai.credentials.basiccredential import BasicCredential

from ccai.errors.exceptions import (
    HttpForbiddenError,
    HttpUnAuthorizedError,
    SemanticError,
)
from ccai.restclient.base.restclientbase import RestClientBase

from ccai.restclient.nsx.aspectsnsx import AspectsNsx, DEFAULT_NSX_ASPECTS
from ccai.restclient.nsx.nsxsession import (
    AUTH_LEAF,
    apply_session_token,
    mint_session_token,
)


_POLICY_PREFIX = "/policy/api/v1/"


# Registry mapping the public property name to (module, class) for the
# Policy API groups exposed on :class:`NsxClient`.
_GROUP_REGISTRY = (
    ("Segments",
        "ccai.restclient.nsx.apigroups.segmentsgroup",
        "SegmentsGroup"),
    ("T0Routers",
        "ccai.restclient.nsx.apigroups.t0routersgroup",
        "T0RoutersGroup"),
    ("T1Routers",
        "ccai.restclient.nsx.apigroups.t1routersgroup",
        "T1RoutersGroup"),
    ("SecurityGroups",
        "ccai.restclient.nsx.apigroups.securitygroupsgroup",
        "SecurityGroupsGroup"),
    ("Dfw",
        "ccai.restclient.nsx.apigroups.dfwgroup",
        "DfwGroup"),
    ("Nat",
        "ccai.restclient.nsx.apigroups.natgroup",
        "NatGroup"),
    ("LoadBalancers",
        "ccai.restclient.nsx.apigroups.loadbalancersgroup",
        "LoadBalancersGroup"),
)


class NsxClient(RestClientBase):
    """
        :class:`RestClientBase` subclass for the NSX-T Manager Policy
        API (``/policy/api/v1/``).

        The client builds the host URL once at construction time,
        exposes its API groups as lazy-cached properties, and overrides
        :meth:`authenticate` to perform NSX-T's form-based session-token
        exchange instead of the default basic-auth dance.
    """

    AUTH_LEAF = AUTH_LEAF

    # NSX-T Manager appliances commonly present self-signed certs in lab
    # environments.  The caller can override per-instance.
    VERIFY_CERTIFICATE = False

    # Re-authenticate transparently when the session token is rejected.
    AUTHENTICATION_FAILURES = (HttpForbiddenError, HttpUnAuthorizedError)

    def __init__(
        self,
        *,
        host: str,
        credential: BaseCredential,
        port: Optional[int] = None,
        scheme: str = "https",
        headers: Optional[Dict[str, str]] = None,
        verify_certificate: Optional[bool] = None,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> None:
        """
            Construct an :class:`NsxClient`.

            :param host: Hostname or IP of the NSX-T Manager.
            :param credential: A :class:`BasicCredential` carrying the
                NSX Manager username / password.
            :param port: Optional non-default port.
            :param scheme: URL scheme, default ``https``.
            :param headers: Optional default headers.
            :param verify_certificate: Override TLS verification.
            :param aspects: Default :class:`AspectsNsx` instance.

            :returns: ``None``

            :raises: SemanticError
        """
        if not isinstance(credential, BasicCredential):
            err_msg_lines = [
                "NsxClient requires a BasicCredential.",
                "GOT: {}".format(type(credential).__name__),
                "EXPECTED: BasicCredential (or compatible subclass)",
            ]
            err_msg = os.linesep.join(err_msg_lines)
            raise SemanticError(err_msg)

        super().__init__(
            host=host,
            credential=credential,
            port=port,
            scheme=scheme,
            headers=headers,
            verify_certificate=verify_certificate,
            aspects=aspects,
        )

        self._group_cache: Dict[str, Any] = {}
        self._auth_lock = threading.Lock()
        self._auth_token: Optional[str] = None
        return

    # ------------------------------------------------------------------
    # URL composition
    # ------------------------------------------------------------------

    def build_url(self, *, leaf: str) -> str:
        """
            Compose an absolute URL for a leaf under the Policy API
            root.

            :param leaf: Leaf path beginning with ``/policy/api/v1/``.

            :returns: The absolute URL.

            :raises: SemanticError
        """
        self._validate_leaf_prefix(leaf=leaf)
        rtnval = "{}{}".format(self._host_url, leaf)
        return rtnval

    @staticmethod
    def _validate_leaf_prefix(*, leaf: str) -> None:
        """
            Ensures a leaf begins with ``/policy/api/v1/``.

            :param leaf: Candidate leaf path.

            :returns: ``None``

            :raises: SemanticError
        """
        if leaf.startswith(_POLICY_PREFIX):
            return None

        err_msg_lines = [
            "NSX leaf must begin with '/policy/api/v1/'.",
            "GOT: {!r}".format(leaf),
        ]
        err_msg = os.linesep.join(err_msg_lines)
        raise SemanticError(err_msg)

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def authenticate(self) -> None:
        """
            Override of :meth:`RestClientBase.authenticate` that
            performs the NSX-T Manager form-based session-token mint.

            :returns: ``None``
        """
        with self._auth_lock:
            session = Session()
            session.verify = self._verify_certificate

            token = mint_session_token(
                session=session,
                base_url=self._host_url,
                credential=self._credential,
                verify_certificate=self._verify_certificate,
            )
            apply_session_token(session=session, token=token)

            self._session = session
            self._auth_token = token
        return None

    def ensure_session(self, *, aspects: AspectsNsx) -> Session:
        """
            Returns the active requests session, minting one on first
            use.

            :param aspects: Behaviour controls (carried for symmetry
                with the rest of the public surface).

            :returns: The :class:`requests.Session` bound to this
                client.
        """
        _ = aspects
        if self._session is None:
            self.authenticate()
        rtnval = self._session
        return rtnval

    @property
    def auth_token(self) -> Optional[str]:
        """
            Cached XSRF token, or ``None`` before first authentication.

            :returns: The token string or ``None``.
        """
        rtnval = self._auth_token
        return rtnval

    # ------------------------------------------------------------------
    # API group access
    # ------------------------------------------------------------------

    def __getattr__(self, name: str) -> Any:
        """
            Lazy-cached property access for API groups.

            Triggered when normal attribute lookup misses; the name is
            looked up in the group registry, the module imported, the
            group constructed, and the instance cached.

            :param name: Attribute name being accessed.

            :returns: The cached group instance.

            :raises: AttributeError
        """
        cache = self.__dict__.get("_group_cache")
        if cache is None:
            err_msg = "{!r} object has no attribute {!r}".format(
                type(self).__name__, name,
            )
            raise AttributeError(err_msg)

        if name in cache:
            rtnval = cache[name]
            return rtnval

        for entry_name, module_path, class_name in _GROUP_REGISTRY:
            if entry_name == name:
                module = __import__(module_path, fromlist=[class_name])
                group_class = getattr(module, class_name)
                instance = group_class(self)
                cache[name] = instance
                rtnval = instance
                return rtnval

        available = sorted(entry[0] for entry in _GROUP_REGISTRY)
        err_msg_lines = [
            "NsxClient has no API group named {!r}.".format(name),
            "AVAILABLE GROUPS:",
        ]
        for grp in available:
            err_msg_lines.append("    {}".format(grp))
        err_msg = os.linesep.join(err_msg_lines)
        raise AttributeError(err_msg)
