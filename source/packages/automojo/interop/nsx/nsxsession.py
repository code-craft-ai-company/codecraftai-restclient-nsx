"""
    .. module:: nsxsession
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: NSX-T Manager session-token mint helpers, separated so
        they can be unit-tested without the full :class:`NsxClient`.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


import os

from http import HTTPStatus

from requests import Session, Response

from automojo.credentials.basiccredential import BasicCredential
from automojo.errors.exceptions import HttpForbiddenError


# NSX-T Manager session-create endpoint.  It is intentionally NOT under
# the ``/policy/api/v1`` prefix; it lives at the appliance root.
AUTH_LEAF = "/api/session/create"

# Header carrying the minted session cookie/token on subsequent calls.
SESSION_COOKIE_NAME = "JSESSIONID"

# NSX-T requires the XSRF token to be echoed back on every mutating call.
XSRF_HEADER = "X-XSRF-TOKEN"


def mint_session_token(
    *,
    session: Session,
    base_url: str,
    credential: BasicCredential,
    verify_certificate: bool,
) -> str:
    """
        POST credentials to the NSX-T Manager session-create endpoint
        and return the minted XSRF token string.

        NSX-T's form-based session login sets a ``JSESSIONID`` cookie on
        the session and returns an ``X-XSRF-TOKEN`` response header.
        Both must accompany subsequent calls; the cookie rides on the
        session jar automatically while the XSRF token is applied to the
        default headers by :func:`apply_session_token`.

        :param session: An open :class:`requests.Session` to POST on.
        :param base_url: The manager host URL (e.g.
            ``https://nsx.example.com``).
        :param credential: Username / password credential.
        :param verify_certificate: TLS verification flag.

        :returns: The minted XSRF token string.

        :raises: HttpForbiddenError
    """
    auth_url = "{}{}".format(base_url.rstrip("/"), AUTH_LEAF)

    form_body = {
        "j_username": credential.username,
        "j_password": credential.password,
    }

    resp: Response = session.post(
        auth_url,
        data=form_body,
        verify=verify_certificate,
    )

    status_code = resp.status_code
    if status_code != HTTPStatus.OK:
        err_msg_lines = [
            "Failed to mint NSX-T Manager session token.",
            "URL: {}".format(auth_url),
            "STATUS: {}".format(status_code),
            "BODY: {!r}".format(resp.content),
        ]
        err_msg = os.linesep.join(err_msg_lines)
        raise HttpForbiddenError(err_msg)

    token = resp.headers.get(XSRF_HEADER)
    if token is None:
        err_msg_lines = [
            "NSX-T session response missing the {!r} header.".format(
                XSRF_HEADER
            ),
            "URL: {}".format(auth_url),
        ]
        err_msg = os.linesep.join(err_msg_lines)
        raise HttpForbiddenError(err_msg)

    rtnval = token
    return rtnval


def apply_session_token(*, session: Session, token: str) -> None:
    """
        Install the minted XSRF token on the session's default headers
        so every subsequent request carries it.

        :param session: The session to mutate.
        :param token: The XSRF token string.

        :returns: ``None``
    """
    session.headers[XSRF_HEADER] = token
    return None
