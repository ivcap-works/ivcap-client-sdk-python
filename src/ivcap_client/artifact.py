#
# Copyright (c) 2023 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
from __future__ import annotations # postpone evaluation of annotations
from typing import TYPE_CHECKING, Dict, Iterator, List, Optional
if TYPE_CHECKING:
    from ivcap_client.ivcap import IVCAP, URN

import datetime
from dataclasses import dataclass
from datetime import datetime

from ivcap_client.api.artifact import artifact_list, artifact_read
from ivcap_client.models.artifact_list_rt import ArtifactListRT
from ivcap_client.models.artifact_status_rt import ArtifactStatusRT
from ivcap_client.models.artifact_list_item import ArtifactListItem
from ivcap_client.models.artifact_status_rt_status import ArtifactStatusRTStatus

from ivcap_client.utils import BaseIter, Links, _set_fields, process_error, set_page
from ivcap_client.aspect import Aspect

@dataclass
class Artifact:
    """This class represents an artifact record
    stored at a particular IVCAP deployment"""

    id: str
    status: ArtifactStatusRTStatus
    name: Optional[str] = None
    size: Optional[int] = None
    mime_type: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    last_modified_at: Optional[datetime.datetime] = None

    etag: Optional[str] = None

    policy: Optional[URN] = None
    account: Optional[URN] = None

    @classmethod
    def _from_list_item(cls, item: ArtifactListItem, ivcap: IVCAP):
        kwargs = item.to_dict()
        return cls(ivcap, **kwargs)

    def __init__(self, ivcap: IVCAP, **kwargs):
        if not ivcap:
            raise ValueError("missing 'ivcap' argument")
        self._ivcap = ivcap
        self.__update__(**kwargs)

    def __update__(self, **kwargs):
        p = ["id", "name", "size", "mime-type", "last-modified-at",
             "created-at", "policy", "etag", "account"]
        hp = ["status", "cache_of", "data_href"]
        _set_fields(self, p, hp, kwargs)

        if not self.id:
            raise ValueError("missing 'id' for Artifact")

    @property
    def urn(self) -> str:
        return self.id

    @property
    def status(self, refresh=True) -> ArtifactStatusRT:
        if refresh or not self._status:
            r = artifact_read.sync_detailed(client=self._ivcap._client, id=self.id)
            if r.status_code >= 300:
                return process_error('place_order', r)
            kwargs = r.parsed.to_dict()
            self.__update__(**kwargs)
        return self._status

    @property
    def metadata(self) -> Iterator[Aspect]:
        return self._ivcap.list_aspect(entity=self.id)

    def add_metadata(self,
                     aspect: Dict[str,any],
                     *,
                     schema: Optional[str]=None,
                     policy: Optional[URN]=None,
    ) -> 'Artifact':
        """Add a metadata 'aspect' to this artifact. The 'schema' of the aspect, if not defined
        is expected to found in the 'aspect' under the '$schema' key.

        Args:
            aspect (dict): The aspect to be attached
            schema (Optional[str], optional): Schema of the aspect. Defaults to 'aspect["$schema"]'.
            policy: Optional[URN]: Set specific policy controlling access ('urn:ivcap:policy:...').

        Returns:
            self: To enable chaining
        """
        self._ivcap.add_aspect(entity=self.id, aspect=aspect, schema=schema, policy=policy)
        return self

    def __repr__(self):
        return f"<Artifact id={self.id}, status={self._status if self._status else '???'}>"

class ArtifactIter(BaseIter[Artifact, ArtifactListItem]):
    def __init__(self, ivcap: 'IVCAP', **kwargs):
        super().__init__(ivcap, **kwargs)

    def _next_el(self, el) -> Artifact:
        return Artifact._from_list_item(el, self._ivcap)

    def _get_list(self) -> List[ArtifactListItem]:
        r = artifact_list.sync_detailed(**self._kwargs)
        if r.status_code >= 300 :
            return process_error('artifact_list', r)
        l: ArtifactListRT = r.parsed
        self._links = Links(l.links)
        return l.items
