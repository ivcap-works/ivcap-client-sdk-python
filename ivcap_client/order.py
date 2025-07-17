#
# Copyright (c) 2023-2025 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
from __future__ import annotations # postpone evaluation of annotations
from typing import TYPE_CHECKING, Dict, List, Optional
if TYPE_CHECKING:
    from ivcap_client.ivcap import IVCAP, URN

import datetime
from dataclasses import dataclass
from datetime import datetime


from ivcap_client.api.order import order_list, order_read
from ivcap_client.aspect import Aspect
from ivcap_client.models.order_list_item import OrderListItem
from ivcap_client.models.order_list_rt import OrderListRT
from ivcap_client.models.order_status_rt import OrderStatusRT
from ivcap_client.models.parameter_t import ParameterT
from ivcap_client.utils import BaseIter, Links, _set_fields, _unset, process_error

@dataclass
class Order:
    """This class represents a particular order placed
    at a particular IVCAP deployment"""

    id: str
    name: Optional[str] = None
    service: Optional[URN] = None
    ordered_at: Optional[datetime.datetime] = None
    started_at: Optional[datetime.datetime] = None
    finished_at: Optional[datetime.datetime] = None

    policy: Optional[URN] = None
    account: Optional[URN] = None

    # products: "PartialProductListT"
    # parameters: List["ParameterT"]
    # tags: Union[Unset, List[str]] = UNSET

    @classmethod
    def _from_list_item(cls, item: OrderListItem, ivcap: IVCAP):
        kwargs = item.to_dict()
        return cls(ivcap, **kwargs)

    def __init__(self, ivcap: IVCAP, **kwargs):
        if not ivcap:
            raise ValueError("missing 'ivcap' argument")
        self._ivcap = ivcap
        self.__update__(**kwargs)

    def __update__(self, **kwargs):
        p = ["id", "name", "service", "ordered_at", "started_at", "finished-at", "policy", "account"]
        hp = ["status"]
        _set_fields(self, p, hp, kwargs)

        self._parameters: Optional[dict[str, ParameterT]] = None
        params = kwargs.get("parameters")
        if params:
            pd = dict(map(lambda d: [d["name"].replace('-', '_'), OrderParameter(ParameterT.from_dict(d))], params))
            pd.pop('cayp_order_id', None) # should not be necessary
            pd.pop('cayp_service_id', None)
            self._parameters = pd


    @property
    def urn(self) -> str:
        return self.id

    def status(self, refresh=True) -> OrderStatusRT:
        if refresh:
            self.refresh()
        return self._status

    @property
    def parameters(self) -> Dict[str, ParameterT]:
        if not self._parameters:
            self.refresh()
        return self._parameters

    def metadata(self) -> List[Aspect]:
        self._ivcap.list_aspect(entity=self.id)

    def add_metadata(self, aspect: Dict[str,any], schema: Optional[str]=None) -> 'Order':
        """Add a metadata 'aspect' to this order. The 'schema' of the aspect, if not defined
        is expected to found in the 'aspect' under the '$schema' key.

        Args:
            aspect (dict): The aspect to be attached
            schema (Optional[str], optional): Schema of the aspect. Defaults to 'aspect["$schema"]'.

        Returns:
            metadata: The metadata record created
        """
        return self._ivcap.add_aspect(entity=self.id, aspect=aspect, schema=schema)

    def refresh(self) -> Order:
        r = order_read.sync_detailed(client=self._ivcap._client, id=self.id)
        if r.status_code >= 300:
            return process_error('place_order', r)
        kwargs = r.parsed.to_dict()
        self.__update__(**kwargs)
        return self

    def __repr__(self):
        status = self._status if self._status else '???'
        return f"<Order id={self.id}, status={status}>"

class OrderIter(BaseIter[Order, OrderListItem]):
    def __init__(self, ivcap: 'IVCAP', **kwargs):
        super().__init__(ivcap, **kwargs)

    def _next_el(self, el) -> Order:
        return Order._from_list_item(el, self._ivcap)

    def _get_list(self) -> List[OrderListItem]:
        r = order_list.sync_detailed(**self._kwargs)
        if r.status_code >= 300 :
            return process_error('artifact_list', r)
        l: OrderListRT = r.parsed
        self._links = Links(l.links)
        return l.items


@dataclass(init=False)
class OrderParameter:
    name: str
    value: any

    def __init__(self, p: ParameterT):
        self.name = _unset(p.name)
        self.value = _unset(p.value)
