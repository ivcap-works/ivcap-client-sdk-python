
from __future__ import annotations # postpone evaluation of annotations 
from typing import List, Optional
import json
from ivcap_client.api.metadata import metadata_list, metadata_read
from ivcap_client.models.list_meta_rt import ListMetaRT
from ivcap_client.models.metadata_list_item_rt import MetadataListItemRT
from ivcap_client.models.metadata_record_rt import MetadataRecordRT

from ivcap_client.utils import process_error, set_page


class Metadata:
    """This class represents a metadata record
    stored at a particular IVCAP deployment"""

    def __init__(self, id: str, ivcap: 'IVCAP', listItem:Optional[MetadataListItemRT]=None):
        self._id = id
        self._ivcap = ivcap
        self._entity = listItem.entity if listItem else None
        self._schema = listItem.schema if listItem else None
        self._aspect = listItem.aspect if listItem else None

    @property
    def urn(self) -> str:
        return self._id

    @property
    def entity(self, refresh=False) -> str:
        if refresh:
            self._refresh()
        return self._entity
    
    @property
    def schema(self, refresh=False) -> str:
        if refresh:
            self._refresh()
        return self._schema

    @property
    def aspect(self, refresh=False) -> dict:
        if refresh:
            self._refresh()
        if isinstance(self._aspect, str):
            s = self._aspect
            self._aspect = json.loads(s)
        return self._aspect

    def _refresh(self):
        r = metadata_read.sync_detailed(self._id, client=self._client)
        if r.status_code >= 300 :
            return process_error('metadata', r)
        res:MetadataRecordRT = r.parsed
        self._entity = res.entity
        self._schema = res.schema
        self._aspect = res.aspect


    def __repr__(self):
        return f"<Metadata id={self._id}, entity={self._entity} schema={self._schema}>"


class MetadataIter:
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
        return Metadata(el.record_id, self._ivcap, el)
        
    def _fill(self) ->  List[MetadataListItemRT]:
        if self._links:
            if not self._links.next_:
                return []
            else:
                self._kwargs['page'] = set_page(self._links.next_)
        r = metadata_list.sync_detailed(**self._kwargs)
        if r.status_code >= 300 :
            return process_error('artifact_list', r)
        l: ListMetaRT = r.parsed
        self._links = l.links
        return l.records