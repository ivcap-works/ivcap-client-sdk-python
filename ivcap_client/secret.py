#
# Copyright (c) 2023-2025 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
from __future__ import annotations # postpone evaluation of annotations
from typing import TYPE_CHECKING, List, Optional, List, Optional

from ivcap_client.models.secret_list_item import SecretListItem
from ivcap_client.models.secret_result_t import SecretResultT

if TYPE_CHECKING:
    from ivcap_client.ivcap import IVCAP, URN

from dataclasses import dataclass

from ivcap_client.api.secret import secret_list, secret_get
from ivcap_client.models.list_meta_rt import ListMetaRT

from ivcap_client.utils import BaseIter, Links, _set_fields, process_error

@dataclass
class Secret:
    """This class represents a secret managed by a particular IVCAP deployment"""

    secret_name: str
    secret_value: str
    expiry_time: int
    secret_type: Optional[str] = None

    @classmethod
    def _from_list_item(cls, item: SecretListItem, ivcap: IVCAP):
        kwargs = item.to_dict()
        return cls(ivcap, **kwargs)

    def __init__(self, ivcap: IVCAP, **kwargs):
        if not ivcap:
            raise ValueError("missing 'ivcap' argument")
        self._ivcap = ivcap
        self.__update__(**kwargs)

    def __update__(self, **kwargs):
        p = ["secret-name", "secret-type", "expiry-time"]
        hp = []
        _set_fields(self, p, hp, kwargs)

    def __repr__(self):
        return f"<Secret name={self.secret_name}>"

class SecretIter(BaseIter[Secret, SecretListItem]):
    def __init__(self, ivcap: 'IVCAP', **kwargs):
        super().__init__(ivcap, **kwargs)

    def _next_el(self, el) -> Secret:
        return Secret._from_list_item(el, self._ivcap)

    def _get_list(self) -> List[SecretListItem]:
        r = secret_list.sync_detailed(**self._kwargs)
        if r.status_code >= 300 :
            return process_error('artifact_list', r)
        l: ListMetaRT = r.parsed
        self._links = Links(l.links)
        return l.items
