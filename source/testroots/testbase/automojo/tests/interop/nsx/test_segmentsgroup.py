"""
    Behavioural tests for :class:`SegmentsGroup` with fully mocked HTTP.
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from automojo.interop.nsx.model.segment import SegmentInfo, SegmentSummary
from automojo.interop.nsx.nsxrealizationhandle import NsxRealizationHandle
from automojo.interop.nsx.specs.segmentspec import SegmentSpec

from automojo.tests.interop.nsx.nsxtestsupport import (
    NSX_BASE,
    make_authenticated_client,
)


_SEGMENTS_URL = NSX_BASE + "/policy/api/v1/infra/segments"


def test_list_single_page(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.get(
        _SEGMENTS_URL,
        json={
            "results": [
                {"id": "seg-a", "display_name": "Segment A"},
                {"id": "seg-b", "display_name": "Segment B"},
            ]
        },
    )
    result = client.Segments.list()
    assert len(result) == 2
    assert isinstance(result[0], SegmentSummary)
    assert result[0].id == "seg-a"
    return


def test_list_follows_cursor(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.get(
        _SEGMENTS_URL,
        [
            {
                "json": {
                    "results": [{"id": "seg-1", "display_name": "S1"}],
                    "cursor": "CUR1",
                }
            },
            {
                "json": {
                    "results": [{"id": "seg-2", "display_name": "S2"}],
                }
            },
        ],
    )
    result = client.Segments.list()
    assert [item.id for item in result] == ["seg-1", "seg-2"]
    assert requests_mock.call_count == 2
    second_query = requests_mock.request_history[1].qs
    assert second_query.get("cursor") == ["cur1"]
    return


def test_get_hits_id_url(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.get(
        _SEGMENTS_URL + "/seg-x",
        json={"id": "seg-x", "display_name": "Segment X"},
    )
    result = client.Segments.get(segment_id="seg-x")
    assert isinstance(result, SegmentInfo)
    assert result.id == "seg-x"
    return


def test_create_or_update_returns_handle(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.patch(
        _SEGMENTS_URL + "/seg-new",
        json={"id": "seg-new", "display_name": "New"},
    )
    spec = SegmentSpec(display_name="New", vlan_ids=[100])
    handle = client.Segments.create_or_update(
        segment_id="seg-new", spec=spec
    )
    assert isinstance(handle, NsxRealizationHandle)
    assert handle.task_id() == "/infra/segments/seg-new"
    body = requests_mock.request_history[0].json()
    assert body["display_name"] == "New"
    assert body["vlan_ids"] == [100]
    return


def test_delete_issues_delete(requests_mock) -> None:
    client = make_authenticated_client()
    requests_mock.delete(_SEGMENTS_URL + "/seg-old", status_code=200)
    client.Segments.delete(segment_id="seg-old")
    assert requests_mock.call_count == 1
    assert requests_mock.request_history[0].method == "DELETE"
    return
