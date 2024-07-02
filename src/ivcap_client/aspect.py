#
# Copyright (c) 2023 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
from __future__ import annotations # postpone evaluation of annotations
from typing import TYPE_CHECKING, Dict, List, Optional, Any, List, Optional, Dict, Set
if TYPE_CHECKING:
    from ivcap_client.ivcap import IVCAP, URN

import datetime
from dataclasses import dataclass, field
from enum import Enum

import json
from ivcap_client.api.aspect import aspect_list, aspect_read
from ivcap_client.models.list_meta_rt import ListMetaRT
from ivcap_client.models.aspect_list_item_rt import AspectListItemRT
from ivcap_client.models.aspect_rt import AspectRT

from ivcap_client.utils import BaseIter, Links, _set_fields, process_error, set_page
from ivcap_client.types import UNSET

@dataclass
class Aspect:
    """This class represents a aspect record
    stored at a particular IVCAP deployment"""

    id: str
    entity: str
    schema: str

    # content: Optional[any] = None
    content_type: Optional[str] = None

    valid_from: Optional[datetime.datetime] = None
    valid_to: Optional[datetime.datetime] = None

    asserter: Optional[URN] = None
    retracter: Optional[URN] = None

    @classmethod
    def _from_list_item(cls, item: AspectListItemRT, ivcap: IVCAP):
        kwargs = item.to_dict()
        return cls(ivcap, **kwargs)

    def __init__(self, ivcap: IVCAP, **kwargs):
        if not ivcap:
            raise ValueError("missing 'ivcap' argument")
        self._ivcap = ivcap
        self.__update__(**kwargs)

    def __update__(self, **kwargs):
        p = ["id", "entity", "schema", "content-type", "valid-from", "valid-to", "asserter", "retracter"]
        hp = ["content"]
        _set_fields(self, p, hp, kwargs)

        c = kwargs.get("content")
        if isinstance(c, dict):
            self._content = c
        else:
            self._content = None

        # self._parameters: Optional[dict[str, ServiceParameter]] = None
        # params = kwargs.get("parameters")
        # if params:
        #     pd = dict(map(lambda d: [d["name"].replace('-', '_'), ServiceParameter(ParameterDefT.from_dict(d))], params))
        #     self._parameters = pd


    # def __init__(self, id: str, ivcap: IVCAP, list_item:Optional[AspectListItemRT]=None):
    #     self._id = id
    #     self._ivcap = ivcap
    #     self._entity = list_item.entity if list_item else None
    #     self._schema = list_item.schema if list_item else None
    #     self._aspect = list_item.content.to_dict() if list_item.content != UNSET else None

    @property
    def urn(self) -> str:
        return self.id

    # @property
    # def entity(self, refresh=False) -> str:
    #     if refresh:
    #         self._refresh()
    #     return self._entity

    # @property
    # def schema(self, refresh=False) -> str:
    #     if refresh:
    #         self._refresh()
    #     return self._schema

    @property
    def aspect(self) -> dict:
        if self._content is None:
            self.refresh()
            # s = self._aspect
            # self._aspect = json.loads(s)
        return self._content

    def refresh(self):
        r = aspect_read.sync_detailed(self.id, client=self._ivcap._client)
        if r.status_code >= 300 :
            return process_error('aspect', r)
        res:AspectRT = r.parsed
        self.__update__(**res.to_dict())


    def __repr__(self):
        return f"<Aspect id={self.id}, entity={self.entity} schema={self.schema}>"


class XAspectIter:
    def __init__(self, ivcap: 'IVCAP', **kwargs):
        self._ivcap = ivcap
        self._kwargs = kwargs
        self._links = None # init navigation
        self._items = self._fill()

    def __iter__(self):
        return self

    def __next__(self):
        if len(self._items) == 0:
            self._items = self._fill()

        if len(self._items) == 0:
            raise StopIteration

        el = self._items.pop(0)
        return Aspect(el.id, self._ivcap, el)

    def _fill(self) ->  List[AspectListItemRT]:
        if self._links:
            if not self._links.next:
                return []
            else:
                self._kwargs['page'] = set_page(self._links.next)
        r = aspect_list.sync_detailed(**self._kwargs)
        if r.status_code >= 300 :
            return process_error('artifact_list', r)
        l: ListMetaRT = r.parsed
        self._links = Links(l.links)
        return l.items

class AspectIter(BaseIter[Aspect, AspectListItemRT]):
    def __init__(self, ivcap: 'IVCAP', **kwargs):
        super().__init__(ivcap, **kwargs)

    def _next_el(self, el) -> Aspect:
        return Aspect._from_list_item(el, self._ivcap)

    def _get_list(self) -> List[AspectListItemRT]:
        r = aspect_list.sync_detailed(**self._kwargs)
        if r.status_code >= 300 :
            return process_error('artifact_list', r)
        l: ListMetaRT = r.parsed
        self._links = Links(l.links)
        return l.items
