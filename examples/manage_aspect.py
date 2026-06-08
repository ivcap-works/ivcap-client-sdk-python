#!/usr/bin/env python3
#
# Copyright (c) 2023-2026 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
"""Example: full aspect lifecycle against a real IVCAP deployment.

Demonstrates:
    1. add_aspect    — attach a new aspect to an entity
    2. list_aspects  — retrieve active aspects by schema
    3. get (refresh) — fetch full aspect content by ID
    4. update_aspect — replace the aspect (retract old + create new atomically)
    5. retract       — explicitly retract the final aspect

At the end of the script **no active aspects are left** on the deployment
for the test entity or schema used here.

Run::

    cd examples/
    export IVCAP_URL=https://your-ivcap-deployment
    export IVCAP_JWT=<your-token>
    python manage_aspect.py
"""

from __future__ import annotations

import sys
import uuid

from _common import ivcap, pp

# ── Configuration ─────────────────────────────────────────────────────────────
# We use a per-run UUID so concurrent test runs never collide.
_RUN_ID = str(uuid.uuid4())
ENTITY_URN = f"urn:example:test:aspect-lifecycle:{_RUN_ID}"
SCHEMA_URN = "urn:example:schema:sdk-test.1"


def main() -> None:
    print(f"\n=== Aspect lifecycle test  (entity={ENTITY_URN!r}) ===\n")

    # ------------------------------------------------------------------
    # 1. Add an aspect
    # ------------------------------------------------------------------
    print("─── 1. add_aspect ───────────────────────────────────────────")
    aspect = ivcap.add_aspect(
        ENTITY_URN,
        {
            "$schema": SCHEMA_URN,
            "name": "sdk-test",
            "version": 1,
            "tags": ["alpha", "beta"],
        },
    )
    print(f"Created : {aspect!r}")
    print(f"  id      : {aspect.id}")
    print(f"  entity  : {aspect.entity}")
    print(f"  schema  : {aspect.schema}")
    print(f"  content : {aspect.content}")

    # ------------------------------------------------------------------
    # 2. List aspects for the entity / schema to confirm it's there
    # ------------------------------------------------------------------
    print("\n─── 2. list_aspects ─────────────────────────────────────────")
    active = list(
        ivcap.list_aspects(
            entity=ENTITY_URN,
            schema=SCHEMA_URN,
            include_content=True,
            limit=5,
        )
    )
    print(f"Found {len(active)} active aspect(s) for entity:")
    for i, a in enumerate(active):
        print(f"  [{i}] {a!r}")
        pp.pprint(a.content)

    # ------------------------------------------------------------------
    # 3. Fetch a single aspect by ID (refresh)
    # ------------------------------------------------------------------
    print("\n─── 3. refresh (get by id) ──────────────────────────────────")
    fetched = aspect.refresh()
    print(f"Refreshed : {fetched!r}")
    print(f"  valid_from : {fetched.valid_from}")
    print(f"  asserter   : {fetched.asserter}")

    # ------------------------------------------------------------------
    # 4. Update the aspect (atomically retracts old, creates new)
    # ------------------------------------------------------------------
    print("\n─── 4. update_aspect ────────────────────────────────────────")
    updated = ivcap.update_aspect(
        ENTITY_URN,
        {
            "$schema": SCHEMA_URN,
            "name": "sdk-test",
            "version": 2,
            "tags": ["alpha", "beta", "gamma"],
            "note": "updated by manage_aspect.py",
        },
    )
    print(f"Updated : {updated!r}")
    print(f"  new id  : {updated.id}")
    print(f"  content : {updated.content}")

    # Confirm old aspect is now retracted
    old = aspect.refresh()
    print(f"\nOld aspect after update: valid_to={old.valid_to!r}  (should be set)")

    # ------------------------------------------------------------------
    # 5. Retract the updated aspect — leave nothing active
    # ------------------------------------------------------------------
    print("\n─── 5. retract ──────────────────────────────────────────────")
    retracted = updated.retract()
    print(f"Retracted : {retracted!r}")
    print(f"  valid_to : {retracted.valid_to!r}  (should be set)")

    # ------------------------------------------------------------------
    # 6. Verify: list_aspects should now return nothing
    # ------------------------------------------------------------------
    print("\n─── 6. verify — no active aspects remain ────────────────────")
    remaining = list(
        ivcap.list_aspects(
            entity=ENTITY_URN,
            schema=SCHEMA_URN,
            include_content=False,
            limit=5,
        )
    )
    if remaining:
        print(f"WARNING: {len(remaining)} aspect(s) still active — expected 0!")
        for a in remaining:
            print(f"  {a!r}")
        sys.exit(1)
    else:
        print("✓  No active aspects remaining — lifecycle test passed.")

    print("\nDone.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
