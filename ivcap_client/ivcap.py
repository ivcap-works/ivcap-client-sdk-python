#
# Copyright (c) 2023-2025 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#

from __future__ import annotations # postpone evaluation of annotations
from datetime import datetime
import os
from typing import IO, Any, Dict, Iterator, Optional
from tusclient.client import TusClient
from sys import maxsize as MAXSIZE
import mimetypes
import base64

from ivcap_client.agent import Agent
from ivcap_client.api.artifact import artifact_upload
from ivcap_client.api.search import search_search
from ivcap_client.artifact import Artifact, ArtifactIter, check_file_already_uploaded, mark_file_already_uploaded
from ivcap_client.aspect import Aspect, AspectIter, _add_update_aspect
from ivcap_client.models.artifact_status_rt import ArtifactStatusRT
from ivcap_client.client.client import AuthenticatedClient, Client
from ivcap_client.exception import AmbiguousRequest, ResourceNotFound
from ivcap_client.order import Order, OrderIter
from ivcap_client.secret import Secret, SecretIter
from ivcap_client.service import Service, ServiceIter
from ivcap_client.types import UNSET, File
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
        inside_platform = False
        if not url:
            url= os.environ.get('IVCAP_URL')
            if not url:
                url= os.environ.get('IVCAP_BASE_URL')
                inside_platform = url is not None
        if not url:
            raise ValueError("missing 'url' argument or environment variables 'IVCAP_URL' or 'IVCAP_BASE_URL' not set.")

        if not token:
            token = os.environ.get('IVCAP_JWT')
        self._url = url
        self._token = token
        self._account_id = account_id
        if inside_platform:
            self._client = Client(base_url=url)
        else:
            if not token:
                raise ValueError("missing 'token' argument or environment variable 'IVCAP_JWT' not set.")
            self._client = AuthenticatedClient(base_url=url, token=token)

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
        """Return a Service instance named 'name'

        Args:
            name (str): Name of service requested

        Raises:
            ResourceNotFound: Service is not found
            AmbiguousRequest: More than one service is found for 'name'

        Returns:
            Service: The Service instance for the requested service
        """
        l = list(self.list_services(filter=f"name~='{name}'"))
        n = len(l)
        if n == 0:
            raise ResourceNotFound(name)
        elif n > 1:
            raise AmbiguousRequest(f"more than one service '{name} found.")
        return l[0]

    def get_service(self, service_id: URN) -> Service:
        """Returns a Service instance for service 'service_id'

        Args:
            service_id (URN): URN of service

        Returns:
            Service: Returns a Service instance if service exists
        """
        return Service(self, id=service_id)

    ### AGENTS

    def get_agent(self, agent_id: URN) -> Agent:
        """Returns an Agent instance for agent 'agent_id'

        Args:
            agent_id (URN): URN of agent

        Returns:
            Service: Returns an Agent instance if agent exists
        """
        return Agent(self, id=agent_id)

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

    def get_order(self, order_id: URN) -> Order:
        """Returns a Service instance for service 'service_id'

        Args:
            order_id (URN): URN of order

        Returns:
            Order: Returns an Order instance if order exists
        """
        return Order(self, id=order_id)

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
        return _add_update_aspect(self, False, entity, aspect, schema=schema, policy=policy)

    def update_aspect(self,
                     entity: str,
                     aspect: Dict[str,any],
                     *,
                     schema: Optional[str]=None,
                     policy: Optional[URN] = None,
                     ) -> Aspect:
        """Create an 'aspect' to an 'entity', but also retract a
        potentially existing aspect for the same entity with the same schema.
        The 'schema' of the aspect, if not defined
        is expected to found in the 'aspect' under the '$schema' key.

        Args:
            entity (str): URN of the entity to attach the aspect to
            aspect (dict): The aspect to be attached
            schema (Optional[str], optional): Schema of the aspect. Defaults to 'aspect["$schema"]'.
            policy: Optional[URN]: Set specific policy controlling access ('urn:ivcap:policy:...').

        Returns:
            aspect: The created aspect record
        """
        return _add_update_aspect(self, True, entity, aspect, schema=schema, policy=policy)

    def list_aspects(self,
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
                        retry_delay: Optional[int] = 30,
                        force_upload: Optional[bool] = False,
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
            force_upload (Optional[bool], optional): Upload file even if it has been uploaded before.
        """

        if not (file_path or io_stream):
            raise ValueError("require either 'file_path' or 'io_stream'")
        if file_path:
            if not (os.path.isfile(file_path) and os.access(file_path, os.R_OK)):
                raise ValueError(f"file '{file_path}' doesn't exist or is not readable.")

        if not force_upload and file_path:
            aurn = check_file_already_uploaded(file_path)
            if aurn is not None:
                return self.get_artifact(aurn)

        if not content_type and file_path:
            content_type, _ = mimetypes.guess_type(file_path)

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
        if file_path:
            mark_file_already_uploaded(res.id, file_path)
        kwargs["status"] = None
        a = Artifact(self, **kwargs)
        a.status # force status update as it will have change
        return a

    def artifact_for_file(self, file_path: str) -> Optional[Artifact]:
        """Return an Artifact instance if local file 'file_path'
        has already been uploaded as artifact.

        Args:
            file_path (str): Path to local file

        Returns:
            Optional[Artifact]: Return artifact instance if file has been uploaded,
            otherwise return None
        """
        aurn = check_file_already_uploaded(file_path)
        if aurn is not None:
            return self.get_artifact(aurn)


    def get_artifact(self, id: URN) -> Artifact:
        """Returns an Artifact instance for artifact 'id'

        Args:
            id (URN): URN of artifact

        Returns:
            Artifact: Returns an Artifact instance if artifact exists
        """
        return Artifact(self, id=id).refresh()

    #### SECRETS

    def list_secrets(self,
            *,
            filter: Optional[str] = None,
            limit: Optional[int] = 10,
            order_by: Optional[str] = None,
            order_desc: Optional[bool] = False,
            at_time: Optional[datetime.datetime] = UNSET,
    ) -> Iterator[Secret]:
        """Return an iterator over all the available secrets fulfilling certain constraints.

        Args:
            limit (Optional[int]): The 'limit' query option sets the maximum number of items
                                    to be included in the result. Default: 10. Example: 10.
            filter_ (Optional[str]): The 'filter' system query option allows clients to filter a
                collection of resources that are addressed by a request URL. The expression specified with 'filter'
                                            is evaluated for each resource in the collection, and only items where the expression
                                            evaluates to true are included in the response. Example: name ~= 'Scott%'.

        Returns:
            Iterator[Secret]: An iterator over a list of secrets

        Yields:
            Secret: A secret object
        """
        kwargs = {
            "filter_": _wrap(filter),
            "limit": _wrap(limit),
            "client": self._client,
        }
        return SecretIter(self, **kwargs)

    #### SEARCH

    def search(self, query):
        """Execute query provided in body and return a list of search result.

        Args:
            at_time (datetime.datetime): Return search which where valid at that time
                [now] Example: 1996-12-19T16:39:57-08:00.
            limit (int): The number of items to be included in the result. Default: 10. Example: 10.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, SearchListRT]]

        """
        body = File(query)
        kwargs = {
            "body": body,
            "content_type": "application/datalog+mangle",
        }
        r = search_search.sync_detailed(client=self._client, **kwargs)
        if r.status_code >= 300:
            raise Exception(f"unexpected response - {r.status_code}")
        return r.parsed

    @property
    def url(self) -> str:
        """Returns the URL of the IVCAP deployment

        Returns:
            str: URL of IVCAP deployment
        """
        return self._url

    def __repr__(self):
        return f"<IVCAP url={self._url}>"
