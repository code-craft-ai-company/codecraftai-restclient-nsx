"""
    Hypothesis property tests for NSX-T URL composition and
    cursor-paging accumulation.
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from hypothesis import given, strategies as st

from automojo.interop.nsx.apigroups.segmentsgroup import SegmentsGroup
from automojo.interop.nsx.aspectsnsx import AspectsNsx
from automojo.interop.nsx.nsxclient import NsxClient

from automojo.tests.interop.nsx.nsxtestsupport import (
    NSX_BASE,
    make_credential,
)


# NSX-T policy ids: alphanumerics, dash, underscore; never empty.
_ID_STRATEGY = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyz0123456789-_",
    min_size=1,
    max_size=24,
)


def _make_client() -> NsxClient:
    rtnval = NsxClient(host="nsx.example.com", credential=make_credential())
    return rtnval


@given(segment_id=_ID_STRATEGY)
def test_compose_url_is_well_formed(segment_id: str) -> None:
    client = _make_client()
    group = SegmentsGroup(client)
    url = group.compose_url(parts=[segment_id])
    expected = NSX_BASE + "/policy/api/v1/infra/segments/" + segment_id
    assert url == expected
    # No accidental double slashes after the scheme.
    assert "//" not in url.split("://", 1)[1]
    return


@given(parts=st.lists(_ID_STRATEGY, min_size=1, max_size=5))
def test_compose_url_always_policy_rooted(parts) -> None:
    client = _make_client()
    group = SegmentsGroup(client)
    url = group.compose_url(parts=parts)
    assert url.startswith(NSX_BASE + "/policy/api/v1/infra/segments/")
    for part in parts:
        assert part in url
    return


@given(
    pages=st.lists(
        st.lists(_ID_STRATEGY, min_size=0, max_size=4),
        min_size=1,
        max_size=6,
    )
)
def test_list_all_accumulates_every_item(pages) -> None:
    client = _make_client()
    group = SegmentsGroup(client)

    # Build a scripted page sequence; every page but the last carries a
    # cursor so list_all keeps fetching.
    sequence = list(pages)
    call_index = {"value": 0}

    def fake_get_json(*, url, aspects, params, context):
        idx = call_index["value"]
        call_index["value"] = idx + 1
        page_items = sequence[idx]
        result = {
            "results": [
                {"id": item, "display_name": item} for item in page_items
            ]
        }
        if idx < len(sequence) - 1:
            result["cursor"] = "cursor-{}".format(idx)
        return result

    group.get_json = fake_get_json

    items = group.list_all(
        url="ignored", aspects=AspectsNsx(), context="prop"
    )
    expected_total = sum(len(page) for page in sequence)
    assert len(items) == expected_total
    return


@given(
    page_size=st.integers(min_value=1, max_value=1000),
    cursor=_ID_STRATEGY,
)
def test_list_all_forwards_paging_params(page_size, cursor) -> None:
    client = _make_client()
    group = SegmentsGroup(client)

    seen_params = []

    def fake_get_json(*, url, aspects, params, context):
        seen_params.append(dict(params))
        if len(seen_params) == 1:
            return {"results": [], "cursor": cursor}
        return {"results": []}

    group.get_json = fake_get_json

    group.list_all(
        url="ignored",
        aspects=AspectsNsx(),
        context="prop",
        page_size=page_size,
    )
    # First call carries page_size, no cursor.
    assert seen_params[0]["page_size"] == page_size
    assert "cursor" not in seen_params[0]
    # Second call carries the cursor returned by page one.
    assert seen_params[1]["cursor"] == cursor
    return
