"""
Patch the downloaded openapi3.json before client generation to fix known upstream
issues in the ivcap-core-api spec that cause openapi-python-client to skip endpoints.

Run from the build/ directory (or pass the JSON path as the first argument).
"""

import json
import sys
import os

spec_path = sys.argv[1] if len(sys.argv) > 1 else "openapi3.json"
spec_path = os.path.abspath(spec_path)

with open(spec_path) as f:
    spec = json.load(f)

patches_applied = []

# ---------------------------------------------------------------------------
# Fix: POST /1/services2/{service_id}/jobs — request body is missing a schema.
# The endpoint accepts any free-form JSON payload, so we add an empty schema
# ({} = any value) so openapi-python-client can generate the endpoint.
# ---------------------------------------------------------------------------
path = "/1/services2/{service_id}/jobs"
try:
    content = spec["paths"][path]["post"]["requestBody"]["content"]
    if "application/json" in content and "schema" not in content["application/json"]:
        content["application/json"]["schema"] = {}
        patches_applied.append(f"Added missing schema to POST {path} requestBody")
except KeyError:
    pass  # path/method doesn't exist — nothing to patch

# ---------------------------------------------------------------------------
# Add further patches here as needed, e.g.:
#   spec["paths"][...]["post"]["requestBody"]["content"]["application/json"]["schema"] = {...}
# ---------------------------------------------------------------------------

with open(spec_path, "w") as f:
    json.dump(spec, f, indent=2)

if patches_applied:
    for msg in patches_applied:
        print(f"[patch_openapi] {msg}")
else:
    print("[patch_openapi] No patches needed.")
