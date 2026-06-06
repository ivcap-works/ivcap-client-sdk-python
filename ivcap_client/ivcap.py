#
# Copyright (c) 2023-2026 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#

from __future__ import annotations  # postpone evaluation of annotations

import os
from collections.abc import Iterator
from datetime import datetime
from sys import maxsize as MAXSIZE
from typing import IO, Any

from ivcap_client.agent import Agent
from ivcap_client.api.search import search_search
from ivcap_client.artifact import (
    Artifact,
    ArtifactIter,
    LocalFileArtifact,
    check_file_already_uploaded,
)
from ivcap_client.aspect import Aspect, AspectIter, _add_update_aspect
from ivcap_client.client.client import AuthenticatedClient, Client
from ivcap_client.collection import (
    Collection,
    CollectionItem,
    CollectionItemIter,
    add_item_to_collection,
    create_collection,
    get_collection,
    list_collections,
    remove_item_from_collection,
    retract_collection,
)
from ivcap_client.exception import AmbiguousRequest, ResourceNotFound
from ivcap_client.order import Order, OrderIter
from ivcap_client.secret import Secret, SecretIter
from ivcap_client.service import Service, ServiceIter
from ivcap_client.types import UNSET, File
from ivcap_client.utils import _wrap, process_error

URN = str


class IVCAP:
    """A class to represent a particular IVCAP deployment and it's capabilities"""

    def __init__(
        self,
        url: str | None = None,
        token: str | None = None,
        account_id: str | None = None,
    ):
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
            url = os.environ.get("IVCAP_URL")
            if not url:
                url = os.environ.get("IVCAP_BASE_URL")
                inside_platform = url is not None
        if not url:
            raise ValueError(
                "missing 'url' argument or environment variables 'IVCAP_URL' or 'IVCAP_BASE_URL' not set."
            )

        if not token:
            token = os.environ.get("IVCAP_JWT")
        self._url = url
        self._token = token
        self._account_id = account_id
        if inside_platform:
            self._client = Client(base_url=url)
        else:
            if not token:
                raise ValueError(
                    "missing 'token' argument or environment variable 'IVCAP_JWT' not set."
                )
            self._client = AuthenticatedClient(base_url=url, token=token)

    #### SERVICES

    def list_services(
        self,
        *,
        filter: str | None = None,
        limit: int | None = 10,
        order_by: str | None = None,
        order_desc: bool | None = False,
        at_time: datetime.datetime | None = UNSET,
    ) -> Iterator[Service]:
        """Return an iterator over all the available services fulfilling certain constraints.

        Args:
            limit (Optional[int]): The 'limit' query option sets the maximum number of items
                                    to be included in the result. Default: 10. Example: 10.
            filter (Optional[str]): The 'filter' system query option allows clients to filter a
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

    def list_orders(
        self,
        *,
        filter: str | None = None,
        limit: int | None = 10,
        order_by: str | None = None,
        order_desc: bool | None = False,
        at_time: datetime.datetime | None = UNSET,
    ) -> Iterator[Order]:
        """Return an iterator over all the available orders fulfilling certain constraints.

        Args:
            limit (Optional[int]): The 'limit' query option sets the maximum number of items
                                    to be included in the result. Default: 10. Example: 10.
            filter (Optional[str]): The 'filter' system query option allows clients to filter a
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

    def add_aspect(
        self,
        entity: str,
        aspect: dict[str, any],
        *,
        schema: str | None = None,
        policy: URN | None = None,
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
        return _add_update_aspect(
            self, False, entity, aspect, schema=schema, policy=policy
        )

    def update_aspect(
        self,
        entity: str,
        aspect: dict[str, any],
        *,
        schema: str | None = None,
        policy: URN | None = None,
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
        return _add_update_aspect(
            self, True, entity, aspect, schema=schema, policy=policy
        )

    def list_aspects(
        self,
        *,
        entity: str | None = None,
        schema: str | None = None,
        content_path: str | None = None,
        at_time: datetime.datetime | None = None,
        limit: int | None = 10,
        filter: str | None = None,
        order_by: str | None = "valid_from",
        order_direction: str | None = "DESC",
        include_content: bool | None = True,
    ) -> Iterator[Aspect]:
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
            filter (Optional[str]): The 'filter' system query option allows clients to filter a collection of
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

    def list_artifacts(
        self,
        *,
        filter: str | None = None,
        limit: int | None = 10,
        order_by: str | None = None,
        order_desc: bool | None = False,
        at_time: datetime.datetime | None = UNSET,
    ) -> Iterator[Artifact]:
        """Return an iterator over all the available artifacts fulfilling certain constraints.

        Args:
            limit (Optional[int]): The 'limit' query option sets the maximum number of items
                                    to be included in the result. Default: 10. Example: 10.
            filter (Optional[str]): The 'filter' system query option allows clients to filter a
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
            Iterator[Artifact]: An iterator over a list of artifacts

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

    def upload_artifact(
        self,
        *,
        name: str | None = None,
        file_path: str | None = None,
        io_stream: IO | None = None,
        content_type: str | None = None,
        content_size: int | None = -1,
        collection: URN | None = None,
        policy: URN | None = None,
        chunk_size: int | None = MAXSIZE,
        retries: int | None = 0,
        retry_delay: int | None = 30,
        force_upload: bool | None = False,
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
        from ivcap_client.artifact import upload_artifact as upload

        return upload(
            self,
            name=name,
            file_path=file_path,
            io_stream=io_stream,
            content_type=content_type,
            content_size=content_size,
            collection=collection,
            policy=policy,
            chunk_size=chunk_size,
            retries=retries,
            retry_delay=retry_delay,
            force_upload=force_upload,
        )

    def artifact_for_file(self, file_path: str) -> Artifact | None:
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
        if id.startswith("file://") or id.startswith("urn:file://"):
            return LocalFileArtifact(id)
        return Artifact(self, id=id).refresh()

    #### COLLECTIONS

    def create_collection(
        self,
        urn: str,
        name: str,
        *,
        description: str | None = None,
        policy: URN | None = None,
    ) -> Collection:
        """Create or update a collection definition (idempotent via PUT).

        Calling this method on an already-existing collection URN **replaces**
        the previous name/description without affecting its items.

        Args:
            urn (str): The collection entity URN
                (e.g. ``urn:ivcap:collection:<uuid>``).
            name (str): Human-readable collection name.
            description (Optional[str]): Optional description.
            policy (Optional[URN]): Access policy URN
                (``urn:ivcap:policy:…``).

        Returns:
            Collection: The created or updated collection.
        """
        return create_collection(
            self, urn, name, description=description, policy=policy
        )

    def get_collection(
        self,
        urn: str,
        *,
        at_time: datetime | None = None,
    ) -> Collection:
        """Fetch a collection definition by its URN.

        Args:
            urn (str): The collection entity URN.
            at_time (Optional[datetime]): Retrieve the state at this point in
                time.

        Returns:
            Collection: The collection instance.

        Raises:
            ResourceNotFound: If no collection with the given URN exists.
        """
        return get_collection(self, urn, at_time=at_time)

    def list_collections(
        self,
        *,
        name_filter: str | None = None,
        limit: int | None = 10,
        at_time: datetime | None = None,
    ) -> Iterator[Collection]:
        """Return an iterator over collection definitions.

        Args:
            name_filter (Optional[str]): A JSONPath comparison expression
                applied to the collection ``name`` field.  The expression is
                wrapped as ``$.name ? (@ <name_filter>)`` before being sent
                to the server.

                Examples::

                    '== "My Ocean Survey"'
                    'starts with "CTD"'
                    'like_regex ".*ocean.*" flag "i"'

            limit (Optional[int]): Maximum number of collections to return.
                Default: 10.
            at_time (Optional[datetime]): Return collections valid at this
                point in time.

        Returns:
            Iterator[Collection]: An iterator over collections.
        """
        return list_collections(
            self, name_filter=name_filter, limit=limit, at_time=at_time
        )

    def add_to_collection(
        self,
        collection_urn: str,
        item_urn: str,
    ) -> CollectionItem | None:
        """Add an item to a collection with automatic deduplication.

        Checks whether *item_urn* is already a member before creating the
        membership aspect.  If it is already present, returns ``None``
        (skip silently).

        Args:
            collection_urn (str): The collection entity URN.
            item_urn (str): URN of the entity to add.

        Returns:
            CollectionItem if the item was newly added, ``None`` if it was
            already a member.
        """
        return add_item_to_collection(self, collection_urn, item_urn)

    def remove_from_collection(
        self,
        collection_urn: str,
        item_urn: str,
    ) -> bool:
        """Remove an item from a collection by retracting its membership aspect.

        Items that are not currently members of the collection are silently
        skipped.

        Args:
            collection_urn (str): The collection entity URN.
            item_urn (str): URN of the entity to remove.

        Returns:
            ``True`` if the membership aspect was retracted, ``False`` if the
            item was not a member.
        """
        return remove_item_from_collection(self, collection_urn, item_urn)

    def retract_collection(
        self,
        collection_urn: str,
    ) -> int:
        """Fully retract a collection and all its item memberships.

        All membership aspects are retracted first (paginated), then the
        collection definition aspect is retracted.  This operation cannot
        be undone.

        Args:
            collection_urn (str): URN of the collection to retract.

        Returns:
            Total number of aspect records retracted (items + 1 definition).

        Raises:
            ResourceNotFound: If no collection definition exists for the URN.
        """
        return retract_collection(self, collection_urn)

    #### SECRETS

    def list_secrets(
        self,
        *,
        filter: str | None = None,
        limit: int | None = 10,
        order_by: str | None = None,
        order_desc: bool | None = False,
        at_time: datetime.datetime | None = UNSET,
    ) -> Iterator[Secret]:
        """Return an iterator over all the available secrets fulfilling certain constraints.

        Args:
            limit (Optional[int]): The 'limit' query option sets the maximum number of items
                                    to be included in the result. Default: 10. Example: 10.
            filter (Optional[str]): The 'filter' system query option allows clients to filter a
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

    def search(self, query: str) -> Any:
        """Execute query provided in body and return a list of search result.

        Args:
            query: The search query to execute.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Search results.

        """
        body = File(query)
        kwargs = {
            "body": body,
            "content_type": "application/datalog+mangle",
        }
        r = search_search.sync_detailed(client=self._client, **kwargs)
        if r.status_code >= 300:
            return process_error("search", r)
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
