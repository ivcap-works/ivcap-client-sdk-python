#
# Copyright (c) 2023 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, Generic, List, Optional, TypeVar
if TYPE_CHECKING:
    from ivcap_client.ivcap import IVCAP, URN


from dataclasses import dataclass
from datetime import datetime
from http.client import HTTPException
from typing import Any, Dict, List, Optional, Union
from .types import UNSET, Response, Unset
from .excpetions import NotAuthorizedException
from urllib.parse import urlparse

def process_error(method: str, r: Response, verbose: bool = True):
    if verbose:
        print(f"Error: {method} failed with {r.status_code} - {r.content}")
    if r.status_code == 401:
        raise NotAuthorizedException()
    raise HTTPException(r.status_code, r.content)

def set_page(next: str):
    u = urlparse(next)
    q = u.query
    if q.startswith("page="):
        return q[len("page="):]
    else:
        raise Exception(f"unexpected 'next' link format - {q}")

@dataclass(frozen=True, init=False)
class Links:
    this: Optional[str] = None
    first: Optional[str] = None
    next: Optional[str] = None

    def __init__(self, la: List[Dict]):
        for e in la:
            if e.rel == "self":
                object.__setattr__(self, "this", e.href)
            elif e.rel == "first":
                object.__setattr__(self, "first", e.href)
            elif e.rel == "next":
                object.__setattr__(self, "next", e.href)

def _unset(v):
    v = None if isinstance(v, Unset) else v
    if v == '':
        v = None
    return v

def _unset_bool(v):
    v = _unset(v)
    return v if v is not None else False

def _wrap(v: Any) -> Union[Unset, any]:
    return v if v is not None else UNSET

def _set_fields(self, attr, hidden_attr, kwargs):
    anno = self.__annotations__
    for k in attr:
        n = k.replace("-", "_")
        v = kwargs.get(k)
        if v is not None and anno[n] == "Optional[datetime.datetime]":
            v = datetime.fromisoformat(v)
        object.__setattr__(self, n, v)

    for k in hidden_attr:
        n = "_" + k.replace("-", "_")
        v = kwargs.get(k)
        object.__setattr__(self, n, v)

T = TypeVar("T")
L = TypeVar("L")

class BaseIter(ABC, Generic[T, L]):
    def __init__(self, ivcap: "IVCAP", **kwargs):
        self._ivcap = ivcap
        self._kwargs = kwargs
        self._links = None # init navigation
        self._remaining = kwargs.get("limit")
        self._items = self._fill()

    def __iter__(self):
        return self

    def __next__(self):
        if self._remaining is not None and self._remaining <= 0:
            raise StopIteration

        if len(self._items) == 0:
            self._items = self._fill()

        if len(self._items) == 0:
            raise StopIteration

        el = self._items.pop(0)
        self._remaining -= 1
        return self._next_el(el)

    def _fill(self) ->  List[L]:
        if self._links:
            if not self._links.next:
                return []
            else:
                self._kwargs['page'] = set_page(self._links.next)
        if self._remaining: self._kwargs['limit'] = self._remaining
        return self._get_list()

    @abstractmethod
    def _next_el(self, el) -> T:
        pass

    @abstractmethod
    def _get_list(self) -> List[L]:
        pass

    # def _get_list()
    #     r = order_list.sync_detailed(**self._kwargs)
    #     if r.status_code >= 300 :
    #         return process_error('artifact_list', r)
    #     l: OrderListRT = r.parsed
    #     self._links = Links(l.links)
    #     return l.items
