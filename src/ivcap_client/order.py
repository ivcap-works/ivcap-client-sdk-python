#
# Copyright (c) 2023 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#

from typing import Dict, List, Optional
from ivcap_client.api.order import order_list, order_read
from ivcap_client.metadata import Metadata
from ivcap_client.models.order_list_item import OrderListItem
from ivcap_client.models.order_list_rt import OrderListRT

from ivcap_client.models.order_status_rt import OrderStatusRT
from ivcap_client.utils import process_error


class Order:
    """This class represents a particular order placed
    at a particular IVCAP deployment"""

    def __init__(self, order_id: str, ivcap: 'IVCAP', status:Optional[OrderStatusRT]=None):
        self._id = order_id
        self._ivcap = ivcap
        self._status = status

    @property
    def urn(self) -> str:
        return self._id

    def status(self, refresh=True) -> OrderStatusRT:
        if refresh or not self._status:
            r = order_read.sync_detailed(client=self._ivcap._client, id=self._id)
            if r.status_code >= 300:
                return process_error('place_order', r)
            self._status = r.parsed
        return self._status

    def metadata(self) -> List[Metadata]:
        self._ivcap.search_metadata(entity=self._id)

    def add_metadata(self, aspect: Dict[str,any], schema: Optional[str]=None) -> 'Order':
        """Add a metadata 'aspect' to this order. The 'schema' of the aspect, if not defined
        is expected to found in the 'aspect' under the '$schema' key.

        Args:
            aspect (dict): The aspect to be attached
            schema (Optional[str], optional): Schema of the aspect. Defaults to 'aspect["$schema"]'.

        Returns:
            metadata: The metadata record created 
        """
        return self._ivcap.add_metadata(entity=self._id, aspect=aspect, schema=schema)

    def __repr__(self):
        status = self._status.status if self._status else 'unknown'
        return f"<Order id={self._id}, status={status}>"
    
class OrderIter:
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
        return Order(el.id, self._ivcap)
        
    def _fill(self) ->  List[OrderListItem]:
        if self._links:
            if not self._links.next_:
                return []
            else:
                self._kwargs['page'] = set_page(self._links.next_)
        r = order_list.sync_detailed(**self._kwargs)
        if r.status_code >= 300 :
            return process_error('artifact_list', r)
        l: OrderListRT = r.parsed
        self._links = l.links
        return l.orders

