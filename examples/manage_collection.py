#!/usr/bin/env python3
#
# Copyright (c) 2023-2026 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
"""Example: manage IVCAP collections.

This script demonstrates how to create, populate, list, and inspect
collections using the IVCAP Python SDK.

Collections are a *virtual* resource backed entirely by DataFabric aspects;
there is no separate REST endpoint.  Two aspect schemas are used internally:

    urn:ivcap:schema:collection.1        — collection definition
    urn:ivcap:schema:collection-item.1   — one membership record per item

Run this example with valid credentials::

    export IVCAP_URL=https://your-ivcap-deployment
    export IVCAP_JWT=<your-token>
    python examples/manage_collection.py
"""

from __future__ import annotations

import sys
import uuid

from client import client  # local helper that builds an IVCAP instance

from ivcap_client import IVCAP, Collection


def main() -> None:
    ivcap: IVCAP = client.ivcap()

    # ------------------------------------------------------------------
    # 1. Create (or update) a collection
    # ------------------------------------------------------------------
    # The collection URN is chosen by the client.  Here we generate a fresh
    # UUID each run; in a real workflow you would store and reuse the URN.
    coll_id = f"urn:ivcap:collection:{uuid.uuid4()}"

    print(f"\n=== Creating collection {coll_id!r} ===")
    coll: Collection = ivcap.create_collection(
        coll_id,
        name="Ocean CTD Survey",
        description="CTD casts from voyage V2025-03",
    )
    print(f"Created: {coll!r}")

    # ------------------------------------------------------------------
    # 2. Add individual item URNs to the collection
    # ------------------------------------------------------------------
    # In a real workflow these URNs would come from uploaded artifacts.
    sample_urns = [
        f"urn:ivcap:artifact:{uuid.uuid4()}",
        f"urn:ivcap:artifact:{uuid.uuid4()}",
        f"urn:ivcap:artifact:{uuid.uuid4()}",
    ]

    print("\n=== Adding items ===")
    for urn in sample_urns:
        result = coll.add_item(urn)
        if result is None:
            print(f"  {urn!r}  →  already a member (skipped)")
        else:
            print(f"  {urn!r}  →  added  (aspect id: {result.id!r})")

    # Adding the same item again demonstrates idempotent deduplication:
    print("\n=== Re-adding first item (dedup check) ===")
    dup = coll.add_item(sample_urns[0])
    print(f"  Result: {'None (already a member)' if dup is None else dup!r}")

    # ------------------------------------------------------------------
    # 3. List all items in the collection
    # ------------------------------------------------------------------
    print("\n=== Items in the collection ===")
    for ci in coll.items(limit=20):
        print(f"  item={ci.item!r}  collection={ci.collection!r}")

    # ------------------------------------------------------------------
    # 4. List all collections (optionally filtered by name)
    # ------------------------------------------------------------------
    print("\n=== All collections (limit 5) ===")
    for c in ivcap.list_collections(limit=5):
        desc = f"  — {c.description}" if c.description else ""
        print(f"  {c.urn!r}  name={c.name!r}{desc}")

    print('\n=== Collections whose name starts with "Ocean" ===')
    for c in ivcap.list_collections(name_filter='starts with "Ocean"', limit=5):
        print(f"  {c.urn!r}  name={c.name!r}")

    # ------------------------------------------------------------------
    # 5. Fetch a specific collection by URN
    # ------------------------------------------------------------------
    print(f"\n=== Fetching collection {coll_id!r} ===")
    fetched = ivcap.get_collection(coll_id)
    print(f"  name        : {fetched.name!r}")
    print(f"  description : {fetched.description!r}")
    print(f"  valid_from  : {fetched.valid_from}")
    print(f"  asserter    : {fetched.asserter}")

    # ------------------------------------------------------------------
    # 6. Add items via ivcap.add_to_collection (module-level API)
    # ------------------------------------------------------------------
    extra_urn = f"urn:ivcap:artifact:{uuid.uuid4()}"
    print(f"\n=== Adding extra item via ivcap.add_to_collection ===")
    result = ivcap.add_to_collection(coll_id, extra_urn)
    print(f"  Added: {result!r}")

    # ------------------------------------------------------------------
    # 7. Remove items from a collection
    # ------------------------------------------------------------------
    print("\n=== Removing items from the collection ===")

    # Remove the first sample artifact
    removed = coll.remove_item(sample_urns[0])
    print(f"  remove_item({sample_urns[0]!r})  →  retracted={removed}")

    # Attempting to remove a non-member is a silent no-op (returns False)
    non_member = f"urn:ivcap:artifact:{uuid.uuid4()}"
    removed_again = coll.remove_item(non_member)
    print(f"  remove_item(<non-member>)  →  retracted={removed_again}  (expected False)")

    # Remove via IVCAP method
    removed_via_ivcap = ivcap.remove_from_collection(coll_id, sample_urns[1])
    print(f"  ivcap.remove_from_collection(...)  →  retracted={removed_via_ivcap}")

    # ------------------------------------------------------------------
    # 8. Retract the entire collection (items + definition)
    # ------------------------------------------------------------------
    print(f"\n=== Retracting entire collection {coll_id!r} ===")
    # coll.retract() is equivalent to ivcap.retract_collection(coll_id)
    total_retracted = coll.retract()
    print(f"  retracted {total_retracted} aspect record(s) total")

    # Alternatively, via the IVCAP method:
    #   total_retracted = ivcap.retract_collection(coll_id)

    print("\nDone.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
