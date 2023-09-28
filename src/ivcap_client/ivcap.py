#
# Copyright (c) 2023 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#

from __future__ import annotations # postpone evaluation of annotations 
from datetime import datetime
import os
import json
from typing import IO, Dict, Iterator, Optional
from ivcap_client.api.artifact import artifact_upload
from ivcap_client.artifact import Artifact, ArtifactIter
from ivcap_client.models.artifact_status_rt import ArtifactStatusRT 
from tusclient.client import TusClient
from sys import maxsize as MAXSIZE
import mimetypes
import base64

from ivcap_client.api.metadata import metadata_add
from ivcap_client.client.client import AuthenticatedClient
from ivcap_client.excpetions import MissingParameterValue
from ivcap_client.metadata import Metadata, MetadataIter
from ivcap_client.models.add_meta_rt import AddMetaRT
from ivcap_client.order import Order, OrderIter
from ivcap_client.service import Service, ServiceIter
from ivcap_client.utils import process_error
from ivcap_client.models.metadata_list_item_rt import MetadataListItemRT

class IVCAP:
    """A class to represent a particular IVCAP deployment and it's capabilities
    """

    def __init__(self, url:Optional[str]=None, token:Optional[str]=None, account_id:Optional[str]=None):
        """Create a new IVCAP instance through which to interact with 
        a specific IVCAP deployment identified by 'url'. Access is authorized
        by 'token'.

        Args:
            url (Optional[str], optional): _description_. Defaults to [env: IVCAP_URL].
            token (Optional[str], optional): _description_. Defaults to [env: IVCAP_JWT].
            account_id (Optional[str], optional): _description_. Defaults to [env: IVCAP_ACCOUNT_ID].
        """
        if not url:
            url= os.getenv('IVCAP_URL', 'https://api.ivcap.net')
        if not token:
            token = os.environ['IVCAP_JWT']
        if not account_id:
            account_id = os.environ['IVCAP_ACCOUNT_ID']
        self._url = url
        self._token = token
        self._client = AuthenticatedClient(base_url=url, token=token)
        self._account_id = account_id

    def list_services(self, 
            filter: Optional[str] = None,
            order_by: Optional[str] = None,
            order_desc: Optional[bool] = False,
            at_time: Optional[datetime.datetime] = None,
    ) -> Iterator[Service]:
        """Return an iterator over all the available services fulfilling certain constraints.

        Args:
            filter Optional[str]: Allows clients to  filter a collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. 
                                        Example: filter=FirstName eq 'Scott'.. Defaults to None.
            order_by Optional[str]: _description_. Defaults to None.
            order_desc Optional[str]: When true sort in descending order otherwise use ascending order. Defaults to False (ascending).
            at_time Optional[datetime.datetime]: Return the list which would have been valid at this time. Defaults to 'Now'.

        Returns:
            Iterator[Service]: An iterator over a list of services

        Yields:
            Service: A Service object
        """
        kwargs = {
            "filter_": filter,
            "order_by": order_by,
            "order_desc": order_desc,
            "at_time": at_time,
            "client": self._client,
        }
        return ServiceIter(self, **kwargs)

    def get_service(self, service_id: str) -> Service:
        return Service(service_id, self)
    
    ### ORDERS

    def list_orders(self, 
            filter: Optional[str] = None,
            order_by: Optional[str] = None,
            order_desc: Optional[bool] = False,
            at_time: Optional[datetime.datetime] = None,
    ) -> Iterator[Order]:
        """Return an iterator over all the available orders fulfilling certain constraints.

        Args:
            filter Optional[str]: Allows clients to  filter a collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. 
                                        Example: filter=FirstName eq 'Scott'.. Defaults to None.
            order_by Optional[str]: _description_. Defaults to None.
            order_desc Optional[str]: When true sort in descending order otherwise use ascending order. Defaults to False (ascending).
            at_time Optional[datetime.datetime]: Return the list which would have been valid at this time. Defaults to 'Now'.

        Returns:
            Iterator[Order]: An iterator over a list of orders

        Yields:
            Order: An order object
        """
        kwargs = {
            "filter_": filter,
            "order_by": order_by,
            "order_desc": order_desc,
            "at_time": at_time,
            "client": self._client,
        }
        return OrderIter(self, **kwargs)    
    
    def get_order(self, id: str) -> Order:
        return Order(id, self)

    #### METADATA

    def add_metadata(self, entity: str, aspect: Dict[str,any], schema: Optional[str]=None) -> Metadata:
        """Add a metadata 'aspect' to 'entity'. The 'schema' of the aspect, if not defined
        is expected to found in the 'aspect' under the '$schema' key.

        Args:
            entity (str): URN of the entity to attach the aspect to
            aspect (dict): The aspect to be attached
            schema (Optional[str], optional): Schema of the aspect. Defaults to 'aspect["$schema"]'.

        Returns:
            metadata: The created metadata record
        """
        if not schema:
            schema = aspect.get("$schema")
        if not schema:
            raise MissingParameterValue("Missing schema (also not in aspect '$schema')")
        kwargs = {
            "entity_id": entity,
            "schema": schema,
            "json_body": aspect, #json.dumps(aspect),
            "client": self._client,
            "content_type": "application/json",
        }
        r = metadata_add.sync_detailed(**kwargs)
        if r.status_code >= 300 :
            return process_error('add_metadata', r)
        
        res:AddMetaRT = r.parsed
        d = res.to_dict()
        d['entity'] = entity
        d['schema'] = schema
        d['aspect'] = aspect
        li = MetadataListItemRT.from_dict(d)
        return Metadata(res.record_id, self, li)
    
    def search_metadata(self,
        *,
        entity: Optional[str] = None,
        schema_prefix : Optional[str] = None,
        aspect_path: Optional[str] = None,
        filter: Optional[str] = None,
        order_by:Optional[str] = None,
        order_desc: Optional[str] = None,
        at_time: Optional[datetime] = None,
    )-> Iterator[Metadata]:
        """Return an iterator over all the metadata records fulfilling certain constraints.

        Args:
            entity Optional[str]: The entity URN for which to restrict the returend metadata records
            schema_prefix Optional[str]: A prefix (using Postgres 'like' patterns) to restrict the 
                                        returend metadata records
            aspect_path: Optional[str]: When defined also return a specific sub tree of the record's aspect
            filter Optional[str]: Allows clients to  filter a collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. 
                                        Example: filter=FirstName eq 'Scott'.. Defaults to None.
            order_by Optional[str]: _description_. Defaults to None.
            order_desc Optional[str]: When true sort in descending order otherwise use ascending order. Defaults to False (ascending).
            at_time Optional[datetime.datetime]: Return the list which would have been valid at this time. Defaults to 'Now'.

        Returns:
            Iterator[Metadata]: An iterator over a list of metadata records

        Yields:
            Metadata: A metadata object
        """
        kwargs = {
            "entity_id": entity,
            "schema": schema_prefix,
            "aspect_path": aspect_path,
            "filter_": filter,
            "order_by": order_by,
            "order_desc": order_desc,
            "at_time": at_time,
            "client": self._client,
        }
        return MetadataIter(self, **kwargs)   

    #### ARTIFACTS

    def list_artifacts(self, 
            filter: Optional[str] = None,
            order_by: Optional[str] = None,
            order_desc: Optional[bool] = False,
            at_time: Optional[datetime.datetime] = None,
    ) -> Iterator[Artifact]:
        """Return an iterator over all the available artifacts fulfilling certain constraints.

        Args:
            filter Optional[str]: Allows clients to  filter a collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. 
                                        Example: filter=FirstName eq 'Scott'.. Defaults to None.
            order_by Optional[str]: _description_. Defaults to None.
            order_desc Optional[str]: When true sort in descending order otherwise use ascending order. Defaults to False (ascending).
            at_time Optional[datetime.datetime]: Return the list which would have been valid at this time. Defaults to 'Now'.

        Returns:
            Iterator[Service]: An iterator over a list of services

        Yields:
            Artifact: An artifact object
        """
        kwargs = {
            "filter_": filter,
            "order_by": order_by,
            "order_desc": order_desc,
            "at_time": at_time,
            "client": self._client,
        }
        return ArtifactIter(self, **kwargs)
    
    def upload_artifact(self,
                        *,
                        name: Optional[str] = None,
                        file_path: Optional[str] = None,
                        io_stream: Optional[IO] = None,
                        content_type:  Optional[str] = None, 
                        content_size: Optional[int] = -1, 
                        chunk_size: Optional[int] = MAXSIZE, 
                        retries: Optional[int] = 0, 
                        retry_delay: Optional[int] = 30
    ) -> Artifact:
        """Uploads content which is either identified as a `file_path` or `io_stream`. In the
        latter case, content type need to be provided.

        Args:
            file_path (Optional[str]): File to upload
            io_stream (Optional[IO]): Content as IO stream. 
            content_type (Optional[str]): Content type - needs to be declared for `io_stream`.
            content_size (Optional[int]): Overall size of content to be uploaded. Defaults to -1 (don't know).
            chunk_size (Optional[int]): Chunk size to use for each individual upload. Defaults to MAXSIZE.
            retries (Optional[int]): The number of attempts should be made in the case of a failed upload. Defaults to 0.
            retry_delay (Optional[int], optional): How long (in seconds) should we wait before retrying a failed upload attempt. Defaults to 30.
        """
        
        if not (file_path or io_stream):
            raise Exception(f"require either 'file_path' or 'io_stream'")

        if not content_type and file_path:
            content_type, encoding= mimetypes.guess_type(file_path) 

        if not content_type:
            raise Exception("missing 'content-type'")
        
        if content_size < 0 and file_path:
            # generate size of file from file_path
            content_size = os.path.getsize(file_path)

        kwargs = {
            'x_content_type': content_type,
            'x_content_length': content_size,
            'tus_resumable': "1.0.0",
        }
        if name:
            n = base64.b64encode(bytes(name, 'utf-8'))
            kwargs['x_name'] = n

        r = artifact_upload.sync_detailed(client=self._client, **kwargs)
        if r.status_code >= 300 :
            return process_error('upload_artifact', r)
        res:ArtifactStatusRT = r.parsed

        h = {'Authorization': f"Bearer {self._token}"}
        data_url = res.data.self_
        c = TusClient(data_url, headers=h)
        kwargs = {
            'file_path': file_path,
            'file_stream': io_stream,
            'chunk_size': chunk_size, 
            'retries': retries, 
            'retry_delay': retry_delay,
        }
        uploader = c.uploader(**kwargs)
        uploader.set_url(data_url) # not sure why I need to set it here again
        uploader.upload()
        a = Artifact(res.id, self)
        a.status # status will have changed after upload
        return a

    def get_artifact(self, id: str) -> Artifact:
        return Artifact(id, self)

    @property
    def url(self) -> str:
        return self._url

    def __repr__(self):
        return f"<IVCAP url={self._url}>"
