#
# Copyright (c) 2023-2026 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
"""Collection support for the IVCAP client.

A **collection** is a named, described grouping of entities (typically artifacts,
but any URN is valid).  Collections are implemented entirely through the
DataFabric aspect store — there is no separate "collection" REST endpoint.

Two aspect schemas govern the feature:

* ``urn:ivcap:schema:collection.1`` — collection definition (name + description)
* ``urn:ivcap:schema:collection-item.1`` — membership record (one per item)

Both aspect types are attached to the **collection entity URN**, i.e. the URN
you choose to represent the collection is used as the ``entity`` field when
creating or querying aspects.
"""

from __future__ import annotations  # postpone evaluation of annotations

import datetime
from collections.abc import Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ivcap_client.api.aspect import aspect_list, aspect_retract
from ivcap_client.aspect import _add_update_aspect
from ivcap_client.exception import MissingParameterValue, ResourceNotFound
from ivcap_client.models.aspect_list_item_rt import AspectListItemRT
from ivcap_client.models.aspect_list_rt import AspectListRT
from ivcap_client.types import UNSET, Unset
from ivcap_client.utils import BaseIter, Links, _wrap, process_error

if TYPE_CHECKING:
    from ivcap_client.ivcap import IVCAP, URN

#: Schema URN for a collection definition aspect.
COLLECTION_SCHEMA = "urn:ivcap:schema:collection.1"

#: Schema URN for a collection-item membership aspect.
COLLECTION_ITEM_SCHEMA = "urn:ivcap:schema:collection-item.1"


# ---------------------------------------------------------------------------
# CollectionItem
# ---------------------------------------------------------------------------


@dataclass
class CollectionItem:
    """A single membership record linking one item to a collection.

    This corresponds to a ``urn:ivcap:schema:collection-item.1`` aspect stored
    in the DataFabric.

    Attributes:
        id:         Aspect record URN.
        collection: Collection entity URN.
        item:       Member entity URN.
        valid_from: Timestamp from which this membership is valid.
        valid_to:   Timestamp until which this membership is valid (``None``
                    if still active).
    """

    id: str
    collection: str
    item: str
    valid_from: datetime.datetime | None = None
    valid_to: datetime.datetime | None = None

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", "")
        self.collection = kwargs.get("collection", "")
        self.item = kwargs.get("item", "")
        vf = kwargs.get("valid_from")
        self.valid_from = vf if not isinstance(vf, Unset) else None
        vt = kwargs.get("valid_to")
        self.valid_to = vt if not isinstance(vt, Unset) else None

    @property
    def urn(self) -> str:
        """Alias for :attr:`item` — the member entity URN."""
        return self.item

    def __repr__(self) -> str:
        return f"<CollectionItem item={self.item!r}, collection={self.collection!r}>"


# ---------------------------------------------------------------------------
# CollectionItemIter
# ---------------------------------------------------------------------------


class CollectionItemIter(BaseIter[CollectionItem, AspectListItemRT]):
    """Iterator over items belonging to a collection.

    Returned by :meth:`Collection.items` and
    :meth:`~ivcap_client.ivcap.IVCAP.list_collection_items`.
    """

    def __init__(self, ivcap: IVCAP, **kwargs):
        super().__init__(ivcap, **kwargs)

    def _next_el(self, el: AspectListItemRT) -> CollectionItem:
        content_dict: dict = {}
        if not isinstance(el.content, Unset):
            content_dict = el.content.to_dict()
        return CollectionItem(
            id=el.id,
            collection=content_dict.get("collection", el.entity),
            item=content_dict.get("item", ""),
            valid_from=el.valid_from,
            valid_to=None if isinstance(el.valid_to, Unset) else el.valid_to,
        )

    def _get_list(self) -> list[AspectListItemRT]:
        r = aspect_list.sync_detailed(**self._kwargs)
        if r.status_code >= 300:
            return process_error("collection_item_list", r)
        parsed: AspectListRT = r.parsed
        self._links = Links(parsed.links)
        return parsed.items


# ---------------------------------------------------------------------------
# Collection
# ---------------------------------------------------------------------------


@dataclass
class Collection:
    """A named, described grouping of entities stored in the IVCAP DataFabric.

    A collection is identified by its **entity URN** and backed by a
    ``urn:ivcap:schema:collection.1`` aspect.  Items are tracked as individual
    ``urn:ivcap:schema:collection-item.1`` aspects attached to the same entity
    URN.

    Attributes:
        urn:         The collection entity URN (also accessible as :attr:`id`).
        name:        Human-readable name.
        description: Optional description.
        asserter:    URN of the account that created/updated the definition.
        valid_from:  Timestamp from which the current definition is valid.
        valid_to:    Timestamp until which the current definition is valid
                     (``None`` if still active).
    """

    urn: str
    name: str
    description: str | None = None
    asserter: URN | None = None
    valid_from: datetime.datetime | None = None
    valid_to: datetime.datetime | None = None

    # NOTE: @dataclass with an explicit __init__ keeps the custom __init__.
    def __init__(self, ivcap: IVCAP, **kwargs):
        if not ivcap:
            raise ValueError("missing 'ivcap' argument")
        self._ivcap = ivcap
        self._update(**kwargs)

    def _update(self, **kwargs) -> None:
        self.urn = kwargs.get("urn") or kwargs.get("entity", "")
        self.name = kwargs.get("name", "")
        self.description = kwargs.get("description")
        self.asserter = kwargs.get("asserter")

        vf = kwargs.get("valid_from")
        if isinstance(vf, str):
            vf = datetime.datetime.fromisoformat(vf)
        self.valid_from = vf if not isinstance(vf, Unset) and vf is not None else None

        vt = kwargs.get("valid_to")
        if isinstance(vt, str):
            vt = datetime.datetime.fromisoformat(vt)
        self.valid_to = vt if not isinstance(vt, Unset) and vt is not None else None

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def id(self) -> str:
        """Alias for :attr:`urn`."""
        return self.urn

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------

    def add_item(self, item_urn: str) -> CollectionItem | None:
        """Add an item to this collection with automatic deduplication.

        Checks whether *item_urn* is already a member before creating the
        membership aspect.  If it is, returns ``None`` (skip silently).

        Args:
            item_urn: URN of the entity to add.

        Returns:
            A :class:`CollectionItem` if the item was newly added, ``None``
            if it was already a member.
        """
        return add_item_to_collection(self._ivcap, self.urn, item_urn)

    def remove_item(self, item_urn: str) -> bool:
        """Remove an item from this collection by retracting its membership aspect.

        Items that are not currently members of the collection are silently
        skipped.

        Args:
            item_urn: URN of the entity to remove.

        Returns:
            ``True`` if the membership aspect was retracted, ``False`` if the
            item was not a member of the collection.
        """
        return remove_item_from_collection(self._ivcap, self.urn, item_urn)

    def items(
        self,
        *,
        limit: int | None = 10,
        at_time: datetime.datetime | None = None,
    ) -> Iterator[CollectionItem]:
        """Return an iterator over all items in this collection.

        Args:
            limit:   Maximum number of items to yield.  Defaults to 10.
            at_time: Return membership records that were valid at this point in
                     time (ISO 8601).  Defaults to *now*.

        Returns:
            An iterator over :class:`CollectionItem` records.
        """
        kwargs = {
            "entity": self.urn,
            "schema": COLLECTION_ITEM_SCHEMA,
            "include_content": True,
            "limit": _wrap(limit),
            "at_time": _wrap(at_time),
            "client": self._ivcap._client,
        }
        return CollectionItemIter(self._ivcap, **kwargs)

    def retract(self) -> int:
        """Fully retract this collection and all its item memberships.

        All membership aspects are retracted first (paginated), then the
        collection definition aspect is retracted.  This operation cannot
        be undone.

        Returns:
            Total number of aspect records retracted (items + 1 definition).
        """
        return retract_collection(self._ivcap, self.urn)

    def refresh(self) -> Collection:
        """Reload the collection definition from IVCAP.

        Returns:
            ``self`` (updated in-place).
        """
        updated = get_collection(self._ivcap, self.urn)
        self._update(
            urn=updated.urn,
            name=updated.name,
            description=updated.description,
            asserter=updated.asserter,
            valid_from=updated.valid_from,
            valid_to=updated.valid_to,
        )
        return self

    def __repr__(self) -> str:
        return f"<Collection urn={self.urn!r}, name={self.name!r}>"


# ---------------------------------------------------------------------------
# CollectionIter
# ---------------------------------------------------------------------------


class CollectionIter(BaseIter[Collection, AspectListItemRT]):
    """Iterator over collection definitions.

    Returned by :meth:`~ivcap_client.ivcap.IVCAP.list_collections`.
    """

    def __init__(self, ivcap: IVCAP, **kwargs):
        super().__init__(ivcap, **kwargs)

    def _next_el(self, el: AspectListItemRT) -> Collection:
        content_dict: dict = {}
        if not isinstance(el.content, Unset):
            content_dict = el.content.to_dict()
        return Collection(
            self._ivcap,
            urn=el.entity,
            name=content_dict.get("name", ""),
            description=content_dict.get("description"),
            asserter=el.additional_properties.get("asserter"),
            valid_from=el.valid_from,
            valid_to=None if isinstance(el.valid_to, Unset) else el.valid_to,
        )

    def _get_list(self) -> list[AspectListItemRT]:
        r = aspect_list.sync_detailed(**self._kwargs)
        if r.status_code >= 300:
            return process_error("collection_list", r)
        parsed: AspectListRT = r.parsed
        self._links = Links(parsed.links)
        return parsed.items


# ---------------------------------------------------------------------------
# Module-level helper functions
# ---------------------------------------------------------------------------


def create_collection(
    ivcap: IVCAP,
    urn: str,
    name: str,
    *,
    description: str | None = None,
    policy: URN | None = None,
) -> Collection:
    """Create or update a collection definition using PUT (idempotent).

    Calling this on an already-existing collection URN **replaces** the
    previous definition (name + description) without affecting its items.

    Args:
        ivcap:       The IVCAP client instance.
        urn:         The collection entity URN (must be a valid IVCAP URN,
                     e.g. ``urn:ivcap:collection:<uuid>``).
        name:        Human-readable collection name.
        description: Optional description.
        policy:      Optional access policy URN
                     (``urn:ivcap:policy:…``).

    Returns:
        A :class:`Collection` representing the created/updated definition.

    Raises:
        :exc:`~ivcap_client.exception.MissingParameterValue`:
            If *urn* or *name* are empty.
    """
    if not urn:
        raise MissingParameterValue("Missing collection URN")
    if not name:
        raise MissingParameterValue("Missing collection name")

    body: dict = {"name": name}
    if description:
        body["description"] = description

    # PUT (is_update=True) ensures idempotency — re-running replaces the old def.
    _add_update_aspect(ivcap, True, urn, body, schema=COLLECTION_SCHEMA, policy=policy)

    return Collection(ivcap, urn=urn, name=name, description=description)


def get_collection(
    ivcap: IVCAP,
    urn: str,
    *,
    at_time: datetime.datetime | None = None,
) -> Collection:
    """Fetch a collection definition from IVCAP.

    Args:
        ivcap:   The IVCAP client instance.
        urn:     The collection entity URN.
        at_time: Retrieve the definition as it was at this point in time.

    Returns:
        A :class:`Collection` instance.

    Raises:
        :exc:`~ivcap_client.exception.ResourceNotFound`:
            If no collection with the given URN exists.
    """
    r = aspect_list.sync_detailed(
        entity=urn,
        schema=COLLECTION_SCHEMA,
        include_content=True,
        limit=2,
        at_time=_wrap(at_time),
        client=ivcap._client,
    )
    if r.status_code >= 300:
        return process_error("get_collection", r)

    parsed: AspectListRT = r.parsed
    if not parsed.items:
        raise ResourceNotFound(urn)

    el = parsed.items[0]
    content_dict: dict = {}
    if not isinstance(el.content, Unset):
        content_dict = el.content.to_dict()

    return Collection(
        ivcap,
        urn=el.entity,
        name=content_dict.get("name", ""),
        description=content_dict.get("description"),
        asserter=el.additional_properties.get("asserter"),
        valid_from=el.valid_from,
        valid_to=None if isinstance(el.valid_to, Unset) else el.valid_to,
    )


def list_collections(
    ivcap: IVCAP,
    *,
    name_filter: str | None = None,
    limit: int | None = 10,
    at_time: datetime.datetime | None = None,
) -> Iterator[Collection]:
    """Return an iterator over collection definitions.

    Args:
        ivcap:       The IVCAP client instance.
        name_filter: Optional JSONPath comparison expression applied to the
                     collection ``name`` field.  The expression is wrapped as
                     ``$.name ? (@ <name_filter>)`` before being sent to the
                     server.

                     Examples::

                         '== "My Ocean Survey"'
                         'starts with "CTD"'
                         'like_regex ".*ocean.*" flag "i"'

        limit:       Maximum number of collections to return.  Defaults to 10.
        at_time:     Return collections that were valid at this point in time.

    Returns:
        An iterator over :class:`Collection` objects.
    """
    content_path: str | None = None
    if name_filter:
        content_path = f"$.name ? (@ {name_filter})"

    kwargs = {
        "schema": COLLECTION_SCHEMA,
        "include_content": True,
        "limit": _wrap(limit),
        "at_time": _wrap(at_time),
        "content_path": _wrap(content_path),
        "client": ivcap._client,
    }
    return CollectionIter(ivcap, **kwargs)


def add_item_to_collection(
    ivcap: IVCAP,
    collection_urn: str,
    item_urn: str,
) -> CollectionItem | None:
    """Add an item to a collection with a prior deduplication check.

    Before creating the membership aspect the server is queried to confirm
    that no active ``collection-item.1`` aspect already records this
    ``(collection, item)`` pair.  If found the call returns ``None`` (skip
    silently).  Otherwise a new aspect record is created with ``POST``.

    Args:
        ivcap:          The IVCAP client instance.
        collection_urn: The collection entity URN.
        item_urn:       URN of the entity to add as a member.

    Returns:
        A :class:`CollectionItem` if the item was added, ``None`` if it
        was already a member.

    Raises:
        :exc:`~ivcap_client.exception.MissingParameterValue`:
            If *collection_urn* or *item_urn* are empty.
    """
    if not collection_urn:
        raise MissingParameterValue("Missing collection URN")
    if not item_urn:
        raise MissingParameterValue("Missing item URN")

    # Dedup check — use JSONPath filter to avoid fetching full content.
    dedup_path = f'$.item ? (@ == "{item_urn}")'
    r = aspect_list.sync_detailed(
        entity=collection_urn,
        schema=COLLECTION_ITEM_SCHEMA,
        content_path=dedup_path,
        include_content=False,
        limit=1,
        client=ivcap._client,
    )
    if r.status_code >= 300:
        return process_error("add_item_to_collection_check", r)

    parsed: AspectListRT = r.parsed
    if parsed.items:
        # Already a member — skip silently.
        return None

    # Create the membership aspect (POST — append, not replace).
    body = {
        "collection": collection_urn,
        "item": item_urn,
    }
    aspect = _add_update_aspect(
        ivcap, False, collection_urn, body, schema=COLLECTION_ITEM_SCHEMA
    )
    return CollectionItem(
        id=aspect.id,
        collection=collection_urn,
        item=item_urn,
    )


def remove_item_from_collection(
    ivcap: IVCAP,
    collection_urn: str,
    item_urn: str,
) -> bool:
    """Remove an item from a collection by retracting its membership aspect.

    Looks up the active ``collection-item.1`` aspect for the
    ``(collection_urn, item_urn)`` pair using a JSONPath filter, then
    retracts it via ``DELETE /1/aspects/<id>``.  Items that are not
    currently members of the collection are silently skipped.

    This operation leaves a retracted (inactive) aspect record in the
    DataFabric — the store is append-only by design.  The item can be
    re-added later by calling :func:`add_item_to_collection` again.

    Args:
        ivcap:          The IVCAP client instance.
        collection_urn: The collection entity URN.
        item_urn:       URN of the entity to remove.

    Returns:
        ``True`` if the membership aspect was found and retracted,
        ``False`` if the item was not a member.

    Raises:
        :exc:`~ivcap_client.exception.MissingParameterValue`:
            If *collection_urn* or *item_urn* are empty.
    """
    if not collection_urn:
        raise MissingParameterValue("Missing collection URN")
    if not item_urn:
        raise MissingParameterValue("Missing item URN")

    # Find the active membership aspect for this item.
    find_path = f'$.item ? (@ == "{item_urn}")'
    r = aspect_list.sync_detailed(
        entity=collection_urn,
        schema=COLLECTION_ITEM_SCHEMA,
        content_path=find_path,
        include_content=False,
        limit=1,
        client=ivcap._client,
    )
    if r.status_code >= 300:
        return process_error("remove_item_from_collection_find", r)

    parsed: AspectListRT = r.parsed
    if not parsed.items:
        # Not a member — skip silently.
        return False

    aspect_id = parsed.items[0].id
    r2 = aspect_retract.sync_detailed(aspect_id, client=ivcap._client)
    if r2.status_code >= 300:
        return process_error("remove_item_from_collection_retract", r2)

    return True


def retract_collection(
    ivcap: IVCAP,
    collection_urn: str,
) -> int:
    """Fully retract a collection and all its item memberships.

    All active ``collection-item.1`` aspects for *collection_urn* are
    retracted first (one ``DELETE`` per membership record, paginated), then
    the ``collection.1`` definition aspect is retracted.

    The DataFabric is append-only — this leaves retracted (inactive) records
    behind but makes the collection invisible to normal queries.  The
    operation cannot be undone.

    Args:
        ivcap:          The IVCAP client instance.
        collection_urn: URN of the collection to retract.

    Returns:
        Total number of aspect records retracted (items + 1 definition).

    Raises:
        :exc:`~ivcap_client.exception.MissingParameterValue`:
            If *collection_urn* is empty.
        :exc:`~ivcap_client.exception.ResourceNotFound`:
            If no collection definition aspect exists for *collection_urn*.
    """
    if not collection_urn:
        raise MissingParameterValue("Missing collection URN")

    retracted = 0

    # ------------------------------------------------------------------
    # Step 1 — retract all collection-item.1 membership aspects
    # ------------------------------------------------------------------
    page_cursor = UNSET
    while True:
        kwargs: dict = {
            "entity": collection_urn,
            "schema": COLLECTION_ITEM_SCHEMA,
            "include_content": False,
            "limit": 50,
            "client": ivcap._client,
        }
        if not isinstance(page_cursor, Unset):
            kwargs["page"] = page_cursor

        r = aspect_list.sync_detailed(**kwargs)
        if r.status_code >= 300:
            return process_error("retract_collection_list_items", r)

        parsed: AspectListRT = r.parsed
        for item in parsed.items:
            r2 = aspect_retract.sync_detailed(item.id, client=ivcap._client)
            if r2.status_code >= 300:
                return process_error("retract_collection_retract_item", r2)
            retracted += 1

        # Advance the pagination cursor.
        links = Links(parsed.links)
        if links.next is None:
            break
        page_cursor = links.next

    # ------------------------------------------------------------------
    # Step 2 — retract the collection definition aspect
    # ------------------------------------------------------------------
    r = aspect_list.sync_detailed(
        entity=collection_urn,
        schema=COLLECTION_SCHEMA,
        include_content=False,
        limit=1,
        client=ivcap._client,
    )
    if r.status_code >= 300:
        return process_error("retract_collection_find_def", r)

    parsed = r.parsed
    if not parsed.items:
        raise ResourceNotFound(collection_urn)

    r2 = aspect_retract.sync_detailed(parsed.items[0].id, client=ivcap._client)
    if r2.status_code >= 300:
        return process_error("retract_collection_retract_def", r2)
    retracted += 1

    return retracted
