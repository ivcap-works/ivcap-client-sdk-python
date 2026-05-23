"""Test configuration.

This repository is often developed with an *installed* `ivcap_client` also present
in the developer environment.

To ensure we test *this checkout* (and not the installed site-packages copy), we
force the repository root onto `sys.path` before test modules are imported.
"""

from __future__ import annotations

import os
import sys


def pytest_configure() -> None:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    # If something imported ivcap_client before we adjusted sys.path, drop it so
    # subsequent imports resolve to the local checkout.
    sys.modules.pop("ivcap_client", None)
