
from typing import Dict, Iterator, List, Optional


from ivcap_client.api.artifact import artifact_list, artifact_read
from ivcap_client.metadata import Metadata
from ivcap_client.models.artifact_list_rt import ArtifactListRT
from ivcap_client.models.artifact_status_rt import ArtifactStatusRT

from ivcap_client.utils import process_error, set_page


class Artifact:
    """This class represents an artifact record
    stored at a particular IVCAP deployment"""

    def __init__(self, id: str, ivcap: 'IVCAP', status:Optional[ArtifactStatusRT]=None):
        self._id = id
        self._ivcap = ivcap
        self._status = status

    @property
    def urn(self) -> str:
        return self._id

    @property
    def status(self, refresh=True) -> ArtifactStatusRT:
        if refresh or not self._status:
            r = artifact_read.sync_detailed(client=self._ivcap._client, id=self._id)
            if r.status_code >= 300:
                return process_error('place_order', r)
            self._status = r.parsed
        return self._status
    
    @property
    def metadata(self) -> Iterator[Metadata]:
        return self._ivcap.search_metadata(entity=self._id)

    def add_metadata(self, aspect: Dict[str,any], schema: Optional[str]=None) -> 'Artifact':
        """Add a metadata 'aspect' to this artifact. The 'schema' of the aspect, if not defined
        is expected to found in the 'aspect' under the '$schema' key.

        Args:
            aspect (dict): The aspect to be attached
            schema (Optional[str], optional): Schema of the aspect. Defaults to 'aspect["$schema"]'.

        Returns:
            self: To enable chaining
        """
        self._ivcap.add_metadata(entity=self._id, aspect=aspect, schema=schema)
        return self
    
    def __repr__(self):
        return f"<Artifact id={self._id}, status={self._status.status if self._status else '???'}>"

class ArtifactIter:
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
        return Artifact(el.id, self._ivcap, el)
        
    def _fill(self) ->  List[ArtifactStatusRT]:
        if self._links:
            if not self._links.next_:
                return []
            else:
                self._kwargs['page'] = set_page(self._links.next_)
        r = artifact_list.sync_detailed(**self._kwargs)
        if r.status_code >= 300 :
            return process_error('artifact_list', r)
        l: ArtifactListRT = r.parsed
        self._links = l.links
        return l.artifacts

