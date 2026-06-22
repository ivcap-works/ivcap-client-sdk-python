#
# Copyright (c) 2023-2026 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#

from __future__ import annotations  # postpone evaluation of annotations

import json
import logging
import mimetypes
import os
import shutil
import uuid
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from sys import maxsize as MAXSIZE
from typing import IO, Any

logger = logging.getLogger(__name__)

from ivcap_client.agent import Agent
from ivcap_client.api.search import search_search
from ivcap_client.artifact import (
    Artifact,
    ArtifactIter,
    LocalAspect,
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
from ivcap_client.exception import (
    AmbiguousRequest,
    MissingParameterValue,
    ResourceNotFound,
)
from ivcap_client.order import Order, OrderIter
from ivcap_client.secret import Secret, SecretIter
from ivcap_client.service import Service, ServiceIter
from ivcap_client.types import UNSET, File
from ivcap_client.utils import _wrap, process_error

URN = str


class IVCAP:
    """A class to represent a particular IVCAP deployment and it's capabilities.

    When no platform URL is available (neither ``url`` argument nor ``IVCAP_URL``/
    ``IVCAP_BASE_URL`` environment variables are set), ``IVCAP()`` transparently
    returns a :class:`~ivcap_client.artifact.LocalIVCAP` instance instead.  This
    means your code does not need to change between local development and deployed
    operation — simply write ``ivcap = IVCAP()`` everywhere:

    .. code-block:: python

        from ivcap_client import IVCAP

        ivcap = IVCAP()  # → LocalIVCAP locally, IVCAP on the platform
        artifact = ivcap.upload_artifact(name="result.csv", file_path="/tmp/result.csv")

    The local artifact root directory is controlled by the ``IVCAP_LOCAL_DIR``
    environment variable (default: ``./data``).
    """

    def __new__(
        cls,
        url: str | None = None,
        token: str | None = None,
        account_id: str | None = None,
    ):
        """Auto-detect platform vs local mode.

        The decision logic is:

        1. If an explicit ``token`` is passed the caller clearly intends to
           connect to a platform — return a normal ``IVCAP`` instance and let
           ``__init__`` raise if the URL is also missing.
        2. Otherwise, check for a platform URL (``url`` arg or ``IVCAP_URL`` /
           ``IVCAP_BASE_URL`` env vars).  If one is found, return a normal
           ``IVCAP`` instance.
        3. If no URL and no explicit token — the environment is unambiguously
           local.  Return a :class:`~ivcap_client.artifact.LocalIVCAP` backed
           by ``IVCAP_LOCAL_DIR`` (default: ``./data``).
        """
        # Explicit token ⇒ platform intent; let __init__ handle validation.
        if token is not None:
            return super().__new__(cls)

        effective_url = (
            url or os.environ.get("IVCAP_URL") or os.environ.get("IVCAP_BASE_URL")
        )
        if not effective_url:
            base_dir = os.environ.get("IVCAP_LOCAL_DIR", "ivcap-artifacts")
            logger.info(
                "No IVCAP platform URL found — using local artifact storage at %r",
                base_dir,
            )
            return LocalIVCAP(base_dir=base_dir)
        # Normal platform instance — Python will call __init__ on this.
        return super().__new__(cls)

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
            # This branch should not be reached in normal use because __new__
            # would have returned a LocalIVCAP already, but guard defensively.
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
        *,
        policy: URN | None = None,
    ) -> CollectionItem | None:
        """Add an item to a collection with automatic deduplication.

        Checks whether *item_urn* is already a member before creating the
        membership aspect.  If it is already present, returns ``None``
        (skip silently).

        Args:
            collection_urn (str): The collection entity URN.
            item_urn (str): URN of the entity to add.
            policy (Optional[URN]): Optional access policy URN for the
                membership aspect (``urn:ivcap:policy:…``).

        Returns:
            CollectionItem if the item was newly added, ``None`` if it was
            already a member.
        """
        return add_item_to_collection(self, collection_urn, item_urn, policy=policy)

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

    @classmethod
    def local(cls, base_dir: str | None = None) -> LocalIVCAP:
        """Return a :class:`~ivcap_client.artifact.LocalIVCAP` instance for
        filesystem-only (no-network) development and testing.

        This is the preferred way to get a local-mode client when you do not
        want to (or cannot) connect to an IVCAP platform deployment:

        .. code-block:: python

            from ivcap_client import IVCAP

            ivcap = IVCAP.local(base_dir="./my-artifacts")
            artifact = ivcap.upload_artifact(name="result.csv", file_path="/tmp/result.csv")

        The ``base_dir`` can also be provided via the ``IVCAP_LOCAL_DIR``
        environment variable.  Precedence (highest first):

        1. The ``base_dir`` argument to this method.
        2. The ``IVCAP_LOCAL_DIR`` environment variable.
        3. The default ``"./data"``.

        Args:
            base_dir: Root directory for artifact storage.  Created on
                demand.  Defaults to ``IVCAP_LOCAL_DIR`` env var, or
                ``"./data"`` if neither is set.

        Returns:
            LocalIVCAP: A filesystem-backed client with the same
            ``upload_artifact`` / ``get_artifact`` interface as :class:`IVCAP`.
        """
        if base_dir is None:
            base_dir = os.environ.get("IVCAP_LOCAL_DIR", "ivcap-artifacts")
        return LocalIVCAP(base_dir=base_dir)

    @property
    def url(self) -> str:
        """Returns the URL of the IVCAP deployment

        Returns:
            str: URL of IVCAP deployment
        """
        return self._url

    def __repr__(self):
        return f"<IVCAP url={self._url}>"


class LocalIVCAP(IVCAP):
    """A filesystem-backed subclass of :class:`IVCAP` for local development
    and testing.  All artifacts are written under ``base_dir``.
    No network calls are made.

    This is the drop-in replacement for :class:`IVCAP` when no IVCAP platform
    URL is available — for example when running a service locally with a test
    JSON file.

    Which implementation is used depends entirely on environment variables:
    ``IVCAP()`` transparently returns a :class:`LocalIVCAP` instance when
    neither ``IVCAP_URL`` nor ``IVCAP_BASE_URL`` is set in the environment,
    and a real :class:`IVCAP` otherwise.

    .. code-block:: python

        from ivcap_client import IVCAP

        ivcap = IVCAP()  # → LocalIVCAP locally, IVCAP on the platform
        artifact = ivcap.upload_artifact(name="report.txt", file_path="/tmp/report.txt")
        print(artifact.id)  # urn:file:///abs/path/to/ivcap-artifacts/report.txt

    The root directory for local artifact storage can also be configured via
    the ``IVCAP_LOCAL_DIR`` environment variable (default: ``ivcap-artifacts``).
    """

    _DEFAULT_BASE_DIR: str = "ivcap-artifacts"

    def __new__(cls, base_dir: str | Path | None = None, **kwargs):
        # Bypass IVCAP.__new__ which performs URL-based dispatch and would
        # otherwise recurse back into LocalIVCAP creation.
        return object.__new__(cls)

    def __init__(self, base_dir: str | Path | None = None):
        """Create a new LocalIVCAP instance.

        Args:
            base_dir: Root directory under which all artifacts and aspects are
                stored.  Relative paths are resolved from the current working
                directory at the time of the first upload.  The directory is
                created on demand.  Defaults to the ``IVCAP_LOCAL_DIR``
                environment variable, or ``"ivcap-artifacts"`` if unset.
        """
        if base_dir is None:
            base_dir = os.environ.get("IVCAP_LOCAL_DIR", self._DEFAULT_BASE_DIR)
        self._base_dir = Path(base_dir)

    # ---- Properties --------------------------------------------------------

    @property
    def base_dir(self) -> Path:
        """The root directory for local artifact and aspect storage."""
        return self._base_dir

    @property
    def _aspects_dir(self) -> Path:
        """Subdirectory used for local aspect storage."""
        return self._base_dir / "aspects"

    @property
    def url(self) -> str:
        """Return a ``file://`` URL pointing at the local base directory."""
        return f"file://{self._base_dir.resolve()}"

    # ---- Artifacts ---------------------------------------------------------

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
        **kwargs,
    ) -> LocalFileArtifact:
        """Write content to the local filesystem and return a :class:`~ivcap_client.artifact.LocalFileArtifact`.

        The content is written to ``<base_dir>/artifacts/<name>``.  Parent
        directories are created automatically (``mkdir -p`` semantics).

        Args:
            name: Relative path under ``base_dir/artifacts/`` for the saved
                artifact.  May contain subdirectory components
                (e.g. ``"results/output.csv"``).  If ``None``, a UUID-based
                filename is generated (preserving the source file extension
                when ``file_path`` is given).
            file_path: Local source file to copy into ``base_dir``.
            io_stream: Byte-stream (or text-stream) to write into ``base_dir``.
                Provide either ``file_path`` or ``io_stream`` — not both.
            content_type: Accepted for interface compatibility; ignored locally.
            content_size: Accepted for interface compatibility; ignored locally.
            collection: Accepted for interface compatibility; silently ignored.
            policy: Accepted for interface compatibility; silently ignored.
            **kwargs: Any additional keyword arguments (e.g. ``chunk_size``,
                ``retries``) are silently ignored so that callers can pass
                platform-specific options without branching.

        Returns:
            LocalFileArtifact: A local-file artifact whose ``.id`` is
            ``urn:file://<absolute_path>``.

        Raises:
            ValueError: If neither ``file_path`` nor ``io_stream`` is provided.
        """
        if not (file_path or io_stream):
            raise ValueError("require either 'file_path' or 'io_stream'")

        if name is None:
            suffix = Path(file_path).suffix if file_path else ""
            name = f"{uuid.uuid4()}{suffix}"

        dest = self._base_dir / "artifacts" / name
        dest.parent.mkdir(parents=True, exist_ok=True)

        if file_path:
            shutil.copy2(file_path, dest)
        else:
            raw = io_stream.read()
            if isinstance(raw, str):
                dest.write_text(raw)
            else:
                dest.write_bytes(raw)

        urn = f"urn:file://{dest.resolve()}"
        logger.info("LocalIVCAP: written artifact '%s' → %s", name, dest)
        return LocalFileArtifact(urn)

    def get_artifact(self, id: str) -> LocalFileArtifact:
        """Return a :class:`~ivcap_client.artifact.LocalFileArtifact` for the given local-file URN.

        Args:
            id: A ``file://`` or ``urn:file://`` URN pointing to a local file.

        Returns:
            LocalFileArtifact: The local file artifact.
        """
        return LocalFileArtifact(id)

    # ---- Aspects -----------------------------------------------------------

    def add_aspect(
        self,
        entity: str,
        aspect: dict,
        *,
        schema: str | None = None,
        policy: URN | None = None,
    ) -> LocalAspect:
        """Store an aspect as a JSON file and return a :class:`~ivcap_client.artifact.LocalAspect`.

        The aspect is written to ``<base_dir>/aspects/<uuid>.json``.
        Each call creates a *new* aspect record (independent of any prior
        records for the same entity/schema pair), matching the additive
        semantics of the platform's ``add_aspect``.

        Args:
            entity: URN of the entity to attach the aspect to.
            aspect: The aspect content dict.  If ``schema`` is ``None``, the
                schema is read from ``aspect["$schema"]``.
            schema: Schema URN.  Defaults to ``aspect["$schema"]``.
            policy: Accepted for interface compatibility; silently ignored.

        Returns:
            LocalAspect: The newly created local aspect record.

        Raises:
            MissingParameterValue: If ``entity`` or schema are missing.
        """
        if not entity:
            raise MissingParameterValue("Missing entity")
        b = dict(aspect) if isinstance(aspect, dict) else aspect.to_dict()
        if not schema:
            schema = b.get("$schema")
        if not schema:
            raise MissingParameterValue("Missing schema (also not in aspect '$schema')")

        aspect_uuid = str(uuid.uuid4())
        aspect_id = f"urn:ivcap:aspect:{aspect_uuid}"
        now = datetime.now(UTC)

        record = {
            "id": aspect_id,
            "entity": entity,
            "schema": schema,
            "content": b,
            "valid_from": now.isoformat(),
            "valid_to": None,
        }

        self._aspects_dir.mkdir(parents=True, exist_ok=True)
        (self._aspects_dir / f"{aspect_uuid}.json").write_text(
            json.dumps(record, indent=2)
        )
        logger.info(
            "LocalIVCAP: written aspect '%s' for entity '%s'", aspect_id, entity
        )
        return LocalAspect(aspect_id, entity, schema, b, valid_from=now)

    def update_aspect(
        self,
        entity: str,
        aspect: dict,
        *,
        schema: str | None = None,
        policy: URN | None = None,
    ) -> LocalAspect:
        """Store an aspect as a JSON file (same as :meth:`add_aspect` locally).

        On the platform ``update_aspect`` retracts any prior aspect with the
        same ``(entity, schema)`` pair before creating the new one.  In local
        mode there is no retraction mechanism, so this method delegates to
        :meth:`add_aspect`.

        Args:
            entity: URN of the entity to attach the aspect to.
            aspect: The aspect content dict.
            schema: Schema URN.  Defaults to ``aspect["$schema"]``.
            policy: Accepted for interface compatibility; silently ignored.

        Returns:
            LocalAspect: The newly created local aspect record.
        """
        return self.add_aspect(entity, aspect, schema=schema, policy=policy)

    def get_aspect(self, aspect_id: str) -> LocalAspect:
        """Return a :class:`~ivcap_client.artifact.LocalAspect` for the given aspect URN or UUID.

        Args:
            aspect_id: Either a full ``urn:ivcap:aspect:<uuid>`` URN or a
                bare UUID string.

        Returns:
            LocalAspect: The stored aspect record.

        Raises:
            ResourceNotFound: If no aspect with the given ID exists on disk.
        """
        prefix = "urn:ivcap:aspect:"
        aspect_uuid = (
            aspect_id[len(prefix) :] if aspect_id.startswith(prefix) else aspect_id
        )

        path = self._aspects_dir / f"{aspect_uuid}.json"
        if not path.exists():
            raise ResourceNotFound(aspect_id)

        record = json.loads(path.read_text())
        valid_from = (
            datetime.fromisoformat(record["valid_from"])
            if record.get("valid_from")
            else None
        )
        return LocalAspect(
            record["id"],
            record["entity"],
            record["schema"],
            record["content"],
            valid_from=valid_from,
        )

    def list_aspects(
        self,
        *,
        entity: str | None = None,
        schema: str | None = None,
        content_path: str | None = None,
        at_time: datetime | None = None,
        limit: int | None = 10,
        filter: str | None = None,
        order_by: str | None = "valid_from",
        order_direction: str | None = "DESC",
        include_content: bool | None = True,
    ) -> Iterator[LocalAspect]:
        """Return an iterator over locally stored aspect records.

        Only ``entity``, ``schema``, and ``limit`` filters are applied in
        local mode; all other parameters are accepted for interface
        compatibility but silently ignored.

        Args:
            entity: Filter by entity URN.
            schema: Filter by schema URN.
            limit: Maximum number of results to return (default: 10).
            content_path, at_time, filter, order_by, order_direction,
                include_content: Accepted for interface compatibility;
                silently ignored locally.

        Yields:
            LocalAspect: Matching aspect records from the local aspects dir.
        """
        if not self._aspects_dir.exists():
            return iter([])

        results = []
        for path in sorted(self._aspects_dir.glob("*.json")):
            if limit is not None and len(results) >= limit:
                break
            try:
                record = json.loads(path.read_text())
            except (json.JSONDecodeError, OSError):
                continue
            if entity and record.get("entity") != entity:
                continue
            if schema and record.get("schema") != schema:
                continue
            valid_from = (
                datetime.fromisoformat(record["valid_from"])
                if record.get("valid_from")
                else None
            )
            results.append(
                LocalAspect(
                    record["id"],
                    record["entity"],
                    record["schema"],
                    record["content"],
                    valid_from=valid_from,
                )
            )
        return iter(results)

    def __repr__(self) -> str:
        return f"<LocalIVCAP base_dir={self._base_dir}>"
