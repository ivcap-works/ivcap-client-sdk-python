#
# Copyright (c) 2023 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#

from __future__ import annotations # postpone evaluation of annotations
from datetime import datetime
import types
import os
from typing import IO, Dict, Iterator, Optional, Union
from ivcap_client.api.artifact import artifact_upload
from ivcap_client.api.aspect import aspect_create
from ivcap_client.artifact import Artifact, ArtifactIter
from ivcap_client.aspect import Aspect, AspectIter
from ivcap_client.models.artifact_status_rt import ArtifactStatusRT
from tusclient.client import TusClient
from sys import maxsize as MAXSIZE
import mimetypes
import base64

from ivcap_client.client.client import AuthenticatedClient
from ivcap_client.excpetions import AmbiguousRequest, MissingParameterValue, ResourceNotFound
from ivcap_client.models.add_meta_rt import AddMetaRT
from ivcap_client.models.aspect_list_item_rt import AspectListItemRT
from ivcap_client.order import Order, OrderIter
from ivcap_client.service import Service, ServiceIter
from ivcap_client.types import UNSET, Unset
from ivcap_client.utils import _wrap, process_error

URN = str

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
            url= os.environ['IVCAP_URL']
        if not token:
            token = os.environ['IVCAP_JWT']
        # if not account_id:
        #     account_id = os.environ['IVCAP_ACCOUNT_ID']
        self._url = url
        self._token = token
        self._client = AuthenticatedClient(base_url=url, token=token)
        self._account_id = account_id

    #### SERVICES

    def list_services(self,
            *,
            filter: Optional[str] = None,
            limit: Optional[int] = 10,
            order_by: Optional[str] = None,
            order_desc: Optional[bool] = False,
            at_time: Optional[datetime.datetime] = UNSET,
    ) -> Iterator[Service]:
        """Return an iterator over all the available services fulfilling certain constraints.

        Args:
            limit (Optional[int]): The 'limit' query option sets the maximum number of items
                                    to be included in the result. Default: 10. Example: 10.
            filter_ (Optional[str]): The 'filter' system query option allows clients to filter a
                collection of resources that are addressed by a request URL. The expression specified with 'filter'
                                            is evaluated for each resource in the collection, and only items where the expression
                                            evaluates to true are included in the response. Example: name ~= 'Scott%'.
            order_by (Optional[str]): The 'orderby' query option allows clients to request
                resources in either
                                    ascending order using asc or descending order using desc. If asc or desc not specified,
                                    then the resources will be ordered in ascending order. The request below orders Trips on
                                    property EndsAt in descending order. Example: orderby=EndsAt.
            order_desc (Optional[bool]): When set order result in descending order. Ascending
                order is the lt. Default: False.
            at_time (Optional[datetime.datetime]): Return the state of the respective resources at
                that time [now] Example: 1996-12-19T16:39:57-08:00.

        Returns:
            Iterator[Service]: An iterator over a list of services

        Yields:
            Service: A Service object
        """
        kwargs = {
            "filter_": _wrap(filter),
            "limit": _wrap(limit),
            "order_by": _wrap(order_by),
            "order_desc": _wrap(order_desc),
            "at_time": _wrap(at_time),
            "client": self._client,
        }
        return ServiceIter(self, **kwargs)

    def get_service_by_name(self, name: str) -> Service:
        l = list(self.list_services(filter=f"name~='{name}'"))
        n = len(l)
        if n == 0:
            raise ResourceNotFound(name)
        elif n > 1:
            raise AmbiguousRequest(f"more than one service '{name} found.")
        return l[0]

    def get_service(self, service_id: URN) -> Service:
        return Service(service_id, self)

    ### ORDERS

    def list_orders(self,
            *,
            filter: Optional[str] = None,
            limit: Optional[int] = 10,
            order_by: Optional[str] = None,
            order_desc: Optional[bool] = False,
            at_time: Optional[datetime.datetime] = UNSET,
    ) -> Iterator[Order]:
        """Return an iterator over all the available orders fulfilling certain constraints.

        Args:
            limit (Optional[int]): The 'limit' query option sets the maximum number of items
                                    to be included in the result. Default: 10. Example: 10.
            filter_ (Optional[str]): The 'filter' system query option allows clients to filter a
                collection of resources that are addressed by a request URL. The expression specified with 'filter'
                                            is evaluated for each resource in the collection, and only items where the expression
                                            evaluates to true are included in the response. Example: name ~= 'Scott%'.
            order_by (Optional[str]): The 'orderby' query option allows clients to request
                resources in either
                                    ascending order using asc or descending order using desc. If asc or desc not specified,
                                    then the resources will be ordered in ascending order. The request below orders Trips on
                                    property EndsAt in descending order. Example: orderby=EndsAt.
            order_desc (Optional[bool]): When set order result in descending order. Ascending
                order is the lt. Default: False.
            at_time (Optional[datetime.datetime]): Return the state of the respective resources at
                that time [now] Example: 1996-12-19T16:39:57-08:00.

        Returns:
            Iterator[Order]: An iterator over a list of orders

        Yields:
            Order: An order object
        """
        kwargs = {
            "filter_": _wrap(filter),
            "limit": _wrap(limit),
            "order_by": _wrap(order_by),
            "order_desc": _wrap(order_desc),
            "at_time": _wrap(at_time),
            "client": self._client,
        }
        return OrderIter(self, **kwargs)

    def get_order(self, id: str) -> Order:
        return Order(id, self)

    #### ASPECT

    def add_aspect(self,
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
            "client": self._client,
            "content_type": "application/json",
        }
        if policy:
            if not policy.startswith("urn:ivcap:policy:"):
                raise ValueError(f"policy '{policy} is not a policy URN.")
            kwargs['policy'] = policy

        r = aspect_create.sync_detailed(**kwargs)
        if r.status_code >= 300 :
            return process_error('add_aspect', r)

        res:AddMetaRT = r.parsed
        d = res.to_dict()
        d['entity'] = entity
        d['schema'] = schema
        d['content'] = aspect
        d['content-type'] = "application/json"
        return Aspect(self, **d)

    def list_aspect(self,
        *,
        entity: Optional[str] = None,
        schema: Optional[str] = None,
        content_path: Optional[str] = None,
        at_time: Optional[datetime.datetime] = None,
        limit: Optional[int] = 10,
        filter: Optional[str] = None,
        order_by: Optional[str] = "valid_from",
        order_direction: Optional[str] = "DESC",
        include_content: Optional[bool] = True,
    )-> Iterator[Aspect]:
        """Return an iterator over all the aspect records fulfilling certain constraints.

        Args:
            entity (Optional[str]): Optional entity for which to request aspects Example:
                urn:blue:image.collA#12.
            schema (Optional[str]): Schema prefix using '%' as wildcard indicator Example:
                urn:blue:schema:image%.
            content_path (Optional[str]): To learn more about the supported format, see
                                                    https://www.postgresql.org/docs/current/datatype-json.html#DATATYPE-JSONPATH Example:
                $.images[*] ? (@.size > 10000).
            at_time (Optional[datetime.datetime]): Return aspect which where valid at that time
                [now] Example: 1996-12-19T16:39:57-08:00.
            limit (Optional[int]): The 'limit' system query option requests the number of items in
                the queried
                                            collection to be included in the result. Default: 10. Example: 10.
            filter_ (Optional[str]): The 'filter' system query option allows clients to filter a collection of
                                            resources that are addressed by a request URL. The expression specified with 'filter'
                                            is evaluated for each resource in the collection, and only items where the expression
                                            evaluates to true are included in the response. Default: ''. Example: FirstName eq
                'Scott'.
            order_by (Optional[str]): Optional comma-separated list of attributes to sort the list
                by.
                * entity
                * schema
                * content
                * policy
                * account
                * created_by
                * retracted_by
                * replaces
                * valid_from
                * valid_to
                Default: 'valid_from'. Example: entity,created-at.
            order_direction (Optional[str]): Set the sort direction 'ASC', 'DESC' for each order-
                by element. Default: 'DESC'. Example: desc.
            include_content (Optional[bool]): When set, also include aspect content in list.

        Returns:
            Iterator[Aspect]: An iterator over a list of aspect records

        Yields:
            Aspect: A aspect object
        """
        kwargs = {
            "entity": _wrap(entity),
            "schema": _wrap(schema),
            "content_path": _wrap(content_path),
            "at_time": _wrap(at_time),
            "limit": _wrap(limit),
            "filter_": _wrap(filter),
            "order_by": _wrap(order_by),
            "order_direction": _wrap(order_direction),
            "include_content": _wrap(include_content),
            "client": self._client,
        }
        return AspectIter(self, **kwargs)

    #### ARTIFACTS

    def list_artifacts(self,
            *,
            filter: Optional[str] = None,
            limit: Optional[int] = 10,
            order_by: Optional[str] = None,
            order_desc: Optional[bool] = False,
            at_time: Optional[datetime.datetime] = UNSET,
    ) -> Iterator[Artifact]:
        """Return an iterator over all the available artifacts fulfilling certain constraints.

        Args:
            limit (Optional[int]): The 'limit' query option sets the maximum number of items
                                    to be included in the result. Default: 10. Example: 10.
            filter_ (Optional[str]): The 'filter' system query option allows clients to filter a
                collection of resources that are addressed by a request URL. The expression specified with 'filter'
                                            is evaluated for each resource in the collection, and only items where the expression
                                            evaluates to true are included in the response. Example: name ~= 'Scott%'.
            order_by (Optional[str]): The 'orderby' query option allows clients to request
                resources in either
                                    ascending order using asc or descending order using desc. If asc or desc not specified,
                                    then the resources will be ordered in ascending order. The request below orders Trips on
                                    property EndsAt in descending order. Example: orderby=EndsAt.
            order_desc (Optional[bool]): When set order result in descending order. Ascending
                order is the lt. Default: False.
            at_time (Optional[datetime.datetime]): Return the state of the respective resources at
                that time [now] Example: 1996-12-19T16:39:57-08:00.

        Returns:
            Iterator[Service]: An iterator over a list of services

        Yields:
            Artifact: An artifact object
        """
        kwargs = {
            "filter_": _wrap(filter),
            "limit": _wrap(limit),
            "order_by": _wrap(order_by),
            "order_desc": _wrap(order_desc),
            "at_time": _wrap(at_time),
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
                        collection: Optional[URN] = None,
                        policy: Optional[URN] = None,
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
            collection: Optional[URN]: Additionally adds artifact to named collection ('urn:...').
            policy: Optional[URN]: Set specific policy controlling access ('urn:ivcap:policy:...').
            chunk_size (Optional[int]): Chunk size to use for each individual upload. Defaults to MAXSIZE.
            retries (Optional[int]): The number of attempts should be made in the case of a failed upload. Defaults to 0.
            retry_delay (Optional[int], optional): How long (in seconds) should we wait before retrying a failed upload attempt. Defaults to 30.
        """

        if not (file_path or io_stream):
            raise ValueError(f"require either 'file_path' or 'io_stream'")

        if not content_type and file_path:
            content_type, encoding= mimetypes.guess_type(file_path)

        if not content_type:
            raise ValueError("missing 'content-type'")

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
        if collection:
            if not collection.startswith("urn:"):
                raise ValueError(f"collection '{collection} is not a URN.")
            kwargs['x_collection'] = collection
        if policy:
            if not policy.startswith("urn:ivcap:policy:"):
                raise ValueError(f"policy '{collection} is not a policy URN.")
            kwargs['x_policy'] = policy

        r = artifact_upload.sync_detailed(client=self._client, **kwargs)
        if r.status_code >= 300 :
            return process_error('upload_artifact', r)
        res:ArtifactStatusRT = r.parsed

        h = {'Authorization': f"Bearer {self._token}"}
        data_url = res.data_href
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

        kwargs = res.to_dict()
        kwargs["status"] = None
        a = Artifact(self, **kwargs)
        a.status # force status update as it will have change
        return a

    def get_artifact(self, id: str) -> Artifact:
        return Artifact(id, self)

    @property
    def url(self) -> str:
        return self._url

    def __repr__(self):
        return f"<IVCAP url={self._url}>"
