#
# Copyright (c) 2023-2025 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
from __future__ import annotations # postpone evaluation of annotations
from typing import TYPE_CHECKING, Dict, List, Optional, List, Optional, Dict

from ivcap_client.exception import MissingParameterValue

if TYPE_CHECKING:
    from ivcap_client.ivcap import IVCAP, URN

import types
import datetime
from dataclasses import dataclass

from ivcap_client.api.aspect import aspect_create, aspect_list, aspect_read, aspect_retract, aspect_update
from ivcap_client.models.list_meta_rt import ListMetaRT
from ivcap_client.models.aspect_list_item_rt import AspectListItemRT
from ivcap_client.models.aspect_rt import AspectRT
from ivcap_client.models.aspect_idrt import AspectIDRT

from ivcap_client.utils import BaseIter, Links, _set_fields, process_error

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

    @property
    def urn(self) -> str:
        return self.id

    @property
    def aspect(self) -> dict:
        if self._content is None:
            self.refresh()
        return self._content

    @property
    def content(self) -> dict:
        return self.aspect

    def refresh(self) -> Aspect:
        r = aspect_read.sync_detailed(self.id, client=self._ivcap._client)
        if r.status_code >= 300 :
            return process_error('aspect', r)
        res:AspectRT = r.parsed
        self.__update__(**res.to_dict())
        return self

    def retract(self) -> Aspect:
        """Retract this aspect"""
        if self.valid_to:
            # already retracted
            return self
        r = aspect_retract.sync_detailed(self.id, client=self._ivcap._client)
        if r.status_code >= 300 :
            return process_error('aspect', r)
        return self.refresh()

    def __repr__(self):
        return f"<Aspect id={self.id}, entity={self.entity} schema={self.schema}>"

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


def _add_update_aspect(ivcap: IVCAP,
                       is_update: bool,
                       entity: str,
                       aspect: Dict[str,any],
                       *,
                       schema: Optional[str]=None,
                       policy: Optional[URN] = None,
                       ) -> Aspect:
    """Add an 'aspect' to an 'entity'. The 'schema' of the aspect, if not defined
    is expected to found in the 'aspect' under the '$schema' key.

    Args:
        entity (str): URN of the entity to attach the aspect to
        aspect (dict): The aspect to be attached
        schema (Optional[str], optional): Schema of the aspect. Defaults to 'aspect["$schema"]'.
        policy: Optional[URN]: Set specific policy controlling access ('urn:ivcap:policy:...').

    Returns:
        aspect: The created aspect record
    """
    if not entity:
        raise MissingParameterValue("Missing entity")
    if isinstance(aspect, dict):
        b = aspect
    else:
        b = aspect.to_dict()

    if not schema:
        schema = b.get("$schema")
    if not schema:
        raise MissingParameterValue("Missing schema (also not in aspect '$schema')")

    b = {
        "$schema": schema,
        "$entity": entity,
        **b
    }
    # api is calling to_dict on body
    body = types.SimpleNamespace()
    body.to_dict = lambda: b

    kwargs = {
        "entity": entity,
        "schema": schema,
        "body": body,
        "client": ivcap._client,
        "content_type": "application/json",
    }
    if policy:
        if not policy.startswith("urn:ivcap:policy:"):
            raise ValueError(f"policy '{policy} is not a policy URN.")
        kwargs['policy'] = policy

    if is_update:
        r = aspect_update.sync_detailed(**kwargs)
    else:
        r = aspect_create.sync_detailed(**kwargs)
    if r.status_code >= 300 :
        return process_error('add_aspect', r)

    res:AspectIDRT = r.parsed
    d = res.to_dict()
    d['entity'] = entity
    d['schema'] = schema
    d['content'] = aspect
    d['content-type'] = "application/json"
    return Aspect(ivcap, **d)