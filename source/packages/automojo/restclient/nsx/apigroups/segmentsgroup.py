"""
    .. module:: segmentsgroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Segments (logical switches) API group for
        :class:`NsxClient`.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import List

from automojo.restclient.nsx.apigroups.basegroup import BaseGroup
from automojo.restclient.nsx.aspectsnsx import AspectsNsx, DEFAULT_NSX_ASPECTS
from automojo.restclient.nsx.model.segment import SegmentInfo, SegmentSummary
from automojo.restclient.nsx.nsxrealizationhandle import NsxRealizationHandle
from automojo.restclient.nsx.specs.segmentspec import SegmentSpec


class SegmentsGroup(BaseGroup):
    """
        Operations on NSX-T segments
        (``/policy/api/v1/infra/segments``).
    """

    BASE_LEAF = "/policy/api/v1/infra/segments"

    def list(
        self,
        *,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> List[SegmentSummary]:
        """
            List every segment defined under ``/infra``.

            :param aspects: Behaviour controls.

            :returns: List of :class:`SegmentSummary`.
        """
        url = self.compose_url()
        items = self.list_all(
            url=url, aspects=aspects, context="SegmentsGroup.list"
        )
        rtnval = [SegmentSummary.from_dict(item) for item in items]
        return rtnval

    def get(
        self,
        *,
        segment_id: str,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> SegmentInfo:
        """
            Retrieve a single segment by id.

            :param segment_id: The segment identifier.
            :param aspects: Behaviour controls.

            :returns: A :class:`SegmentInfo`.
        """
        url = self.compose_url(parts=[segment_id])
        body = self.get_json(
            url=url, aspects=aspects, context="SegmentsGroup.get"
        )
        rtnval = SegmentInfo.from_dict(body)
        return rtnval

    def create_or_update(
        self,
        *,
        segment_id: str,
        spec: SegmentSpec,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> NsxRealizationHandle:
        """
            Create or update a segment (NSX-T policy upsert via PATCH).

            :param segment_id: The segment identifier.
            :param spec: A :class:`SegmentSpec` describing the segment.
            :param aspects: Behaviour controls.

            :returns: An :class:`NsxRealizationHandle` tracking
                realization of the intent.
        """
        url = self.compose_url(parts=[segment_id])
        self.patch_json(
            url=url,
            body=spec.to_dict(),
            aspects=aspects,
            context="SegmentsGroup.create_or_update",
        )
        intent_path = "/infra/segments/{}".format(segment_id)
        rtnval = NsxRealizationHandle(
            intent_path=intent_path, client=self.client
        )
        return rtnval

    def delete(
        self,
        *,
        segment_id: str,
        aspects: AspectsNsx = DEFAULT_NSX_ASPECTS,
    ) -> None:
        """
            Delete a segment by id.

            :param segment_id: The segment identifier.
            :param aspects: Behaviour controls.

            :returns: ``None``
        """
        url = self.compose_url(parts=[segment_id])
        self.delete_resource(
            url=url, aspects=aspects, context="SegmentsGroup.delete"
        )
        return None
