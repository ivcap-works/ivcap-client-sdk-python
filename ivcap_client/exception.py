#
# Copyright (c) 2023-2026 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


class IvcapError(Exception):
    """Base class for all IVCAP client exceptions."""


@dataclass
class IvcapApiError(IvcapError):
    """Represents an HTTP error returned by the IVCAP API.

    This exception is intended to be raised by the *core* convenience layer.
    The generated `ivcap_client.api.*` functions may raise
    `ivcap_client.errors.UnexpectedStatus` instead.
    """

    operation: str
    status_code: int
    content: Any = None
    url: str | None = None
    headers: Mapping[str, Any] | None = None

    def __str__(self) -> str:
        parts = [f"{self.operation} failed with HTTP {self.status_code}"]
        if self.url:
            parts.append(f"url={self.url}")

        msg = " (" + ", ".join(parts[1:]) + ")" if len(parts) > 1 else ""
        body = _safe_decode_content(self.content)
        if body:
            return f"{parts[0]}{msg}: {body}"
        return f"{parts[0]}{msg}"


class NotAuthorizedException(IvcapApiError):
    """Raised when the request is not authorized (typically HTTP 401/403)."""

    def __init__(
        self,
        operation: str,
        status_code: int = 401,
        content: Any = None,
        url: str | None = None,
        headers: Mapping[str, Any] | None = None,
    ):
        super().__init__(
            operation=operation,
            status_code=status_code,
            content=content,
            url=url,
            headers=headers,
        )


class ResourceNotFound(Exception):
    """Exception raised when requestred resource is not found.

    Attributes:
        resource: name or URN of missing resource
    """

    def __init__(self, resource: str):
        self.resource = resource
        self.message = f"resource '{resource}' not found"
        super().__init__(self.message)


class AmbiguousRequest(Exception):
    """Exception raised when request is not specific enough.

    Attributes:
        message: cause for ambiguity
    """

    def __init__(self, message: str):
        super().__init__(message)


class MissingParameterValue(Exception):
    pass


class HttpException(IvcapApiError):
    """Backward compatible alias for :class:`IvcapHttpError`."""


def _safe_decode_content(content: Any, *, limit: int = 4096) -> str:
    """Return a readable string for HTTP response content.

    - bytes are decoded as UTF-8 with replacement
    - other objects are coerced to str
    - result is truncated to `limit` characters
    """
    if content is None:
        return ""

    try:
        if isinstance(content, (bytes, bytearray)):
            s = bytes(content).decode("utf-8", errors="replace")
        else:
            s = str(content)
    except Exception:
        s = ""

    if len(s) > limit:
        return s[:limit] + "…"
    return s
