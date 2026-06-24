"""
MkDocs hook: inject the closest git tag as ``config.extra.version_tag``.

This is used by the ``overrides/partials/source.html`` template to display
the version tag next to the GitHub repository link in the site header,
replacing the default branches / stars count shown by Material for MkDocs.
"""

from __future__ import annotations

import os
import subprocess


def on_config(config, **kwargs):
    """Populate ``config.extra['version_tag']`` before the build starts."""
    config.extra["version_tag"] = _get_version_tag()
    return config


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_version_tag() -> str:
    """Return the closest annotated or lightweight git tag, or fall back to
    the version field in ``pyproject.toml``.
    """
    # mkdocs runs from the docs/ directory, so the project root is one level up
    project_root = os.path.join(os.path.dirname(__file__), "..")

    # 1. Try git describe
    try:
        tag = subprocess.check_output(
            ["git", "describe", "--abbrev=0", "--tags"],
            text=True,
            stderr=subprocess.DEVNULL,
            cwd=project_root,
        ).strip()
        if tag:
            return tag
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # 2. Fall back to pyproject.toml version field
    try:
        import tomllib  # Python 3.11+
    except ImportError:
        try:
            import tomli as tomllib  # type: ignore[no-redef]
        except ImportError:
            return "latest"

    try:
        pyproject = os.path.join(project_root, "pyproject.toml")
        with open(pyproject, "rb") as fh:
            data = tomllib.load(fh)
        version = data["tool"]["poetry"]["version"]
        return f"v{version}"
    except Exception:
        return "latest"
