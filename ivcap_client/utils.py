#
# Copyright (c) 2023-2026 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, Optional, TypeVar, Union

from pydantic import BaseModel

if TYPE_CHECKING:
    from ivcap_client.ivcap import IVCAP


from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlparse

from .exception import IvcapApiError, NotAuthorizedException
from .types import UNSET, Response, Unset


def process_error(method: str, r: Response, verbose: bool = True):
    """Raise an exception for an unsuccessful HTTP response.

    Note: This function intentionally raises SDK-specific exceptions rather than
    `http.client.HTTPException`.
    """

    # Preserve backward compatibility of the `verbose` argument by still
    # emitting something, but avoid printing directly to stdout.
    # Users can configure logging handlers/levels as desired.
    if verbose:
        import logging

        logging.getLogger(__name__).error(
            "Error: %s failed with %s - %s",
            method,
            getattr(r, "status_code", "?"),
            getattr(r, "content", None),
        )

    status = int(getattr(r, "status_code", 0) or 0)
    content = getattr(r, "content", None)
    url = str(getattr(getattr(r, "request", None), "url", None) or "") or None
    headers = getattr(r, "headers", None)

    if status in (401, 403):
        raise NotAuthorizedException(
            method, status_code=status, content=content, url=url, headers=headers
        )

    raise IvcapApiError(method, status, content=content, url=url, headers=headers)


def set_page(next: str):
    u = urlparse(next)
    q = u.query
    if q.startswith("page="):
        return q[len("page=") :]
    else:
        raise Exception(f"unexpected 'next' link format - {q}")


@dataclass(frozen=True, init=False)
class Links:
    this: str | None = None
    first: str | None = None
    next: str | None = None

    def __init__(self, la: list[dict]):
        for e in la:
            if e.rel == "self":
                object.__setattr__(self, "this", e.href)
            elif e.rel == "first":
                object.__setattr__(self, "first", e.href)
            elif e.rel == "next":
                object.__setattr__(self, "next", e.href)


def _unset(v):
    v = None if isinstance(v, Unset) else v
    if v == "":
        v = None
    return v


def _unset_bool(v):
    v = _unset(v)
    return v if v is not None else False


def _wrap(v: Any) -> Unset | Any:
    return v if v is not None else UNSET


def _set_fields(self, attr, hidden_attr, kwargs):
    anno = self.__annotations__
    for k in attr:
        n = k.replace("-", "_")
        v = kwargs.get(k)
        if v is not None and anno[n] == "Optional[datetime.datetime]":
            v = datetime.fromisoformat(v)
        object.__setattr__(self, n, v)

    for k in hidden_attr:
        n = "_" + k.replace("-", "_")
        v = kwargs.get(k)
        object.__setattr__(self, n, v)


T = TypeVar("T")
L = TypeVar("L")


class BaseIter(ABC, Generic[T, L]):
    def __init__(self, ivcap: "IVCAP", **kwargs):
        self._ivcap = ivcap
        self._kwargs = kwargs
        self._links = None  # init navigation
        self._remaining = (
            kwargs.get("limit") if not isinstance(kwargs.get("limit"), Unset) else None
        )
        self._items = self._fill()

    def __iter__(self):
        return self

    def __next__(self):
        if self._remaining is not None and self._remaining <= 0:
            raise StopIteration

        if len(self._items) == 0:
            self._items = self._fill()

        if len(self._items) == 0:
            raise StopIteration

        el = self._items.pop(0)
        if self._remaining:
            self._remaining -= 1
        return self._next_el(el)

    def _fill(self) -> list[L]:
        if self._links:
            if not self._links.next:
                return []
            else:
                self._kwargs["page"] = set_page(self._links.next)
        limit = self._remaining if self._remaining and self._remaining <= 50 else 50
        self._kwargs["limit"] = limit
        return self._get_list()

    def has_next(self) -> bool:
        if self._remaining != None and self._remaining <= 0:
            return False
        if len(self._items) == 0 and self._links and not self._links.next:
            return False
        return True

    @abstractmethod
    def _next_el(self, el) -> T:
        pass

    @abstractmethod
    def _get_list(self) -> list[L]:
        pass


def model_from_json_schema(
    schema: dict, model_name: str = "DynamicModel", root_schema: dict = None
) -> type[BaseModel]:
    """Generate a pydantic model from a json schema definition, with $ref/$defs support."""

    from enum import Enum

    from pydantic import create_model

    if root_schema is None:
        root_schema = schema

    def resolve_ref(ref: str):
        # Only supports local refs like "#/$defs/Name"
        if not ref.startswith("#/"):
            raise NotImplementedError(f"Only local refs are supported, got: {ref}")
        parts = ref.lstrip("#/").split("/")
        obj = root_schema
        for part in parts:
            obj = obj[part]
        return obj

    def parse_type(details, prop_name=None, parent_name=""):
        # Handle $ref
        if "$ref" in details:
            ref_schema = resolve_ref(details["$ref"])
            return parse_type(ref_schema, prop_name, parent_name)

        # Handle enums
        if "enum" in details:
            enum_name = f"{parent_name}_{prop_name}_Enum" if prop_name else "Enum"
            enum_values = details["enum"]
            enum_type = type(enum_name, (Enum,), {str(v): v for v in enum_values})
            return enum_type

        # Handle anyOf/oneOf for unions and optionals
        if "anyOf" in details or "oneOf" in details:
            variants = details.get("anyOf", details.get("oneOf"))
            types = []
            has_null = False
            for v in variants:
                # $ref or type
                if "$ref" in v:
                    t = parse_type(v, prop_name, parent_name)
                else:
                    t = v.get("type")
                    if t == "null":
                        has_null = True
                        continue
                    t = parse_type(v, prop_name, parent_name)
                types.append(t)
            if has_null:
                if len(types) == 1:
                    return Optional[types[0]]
                else:
                    return Optional[tuple(types)]
            else:
                if len(types) == 1:
                    return types[0]
                else:
                    return Union[tuple(types)]

        # Handle arrays
        if details.get("type") == "array":
            items = details.get("items", {})
            item_type = parse_type(items, prop_name, parent_name)
            return list[item_type]

        # Handle objects (nested models)
        if details.get("type") == "object":
            # Recursively create nested model
            nested_model_name = (
                f"{parent_name}_{prop_name}_Model" if prop_name else "NestedModel"
            )
            nested_model = model_from_json_schema(
                details, nested_model_name, root_schema
            )
            return nested_model

        # Handle primitive types
        t = details.get("type")
        if t == "string":
            return str
        elif t == "integer":
            return int
        elif t == "number":
            return float
        elif t == "boolean":
            return bool
        else:
            return str  # fallback

    fields = {}
    required = set(schema.get("required", []))
    properties = schema.get("properties", {})
    for prop, details in properties.items():
        typ = parse_type(details, prop, model_name)
        default = details.get("default", ...)
        # Set required/optional and default
        if prop not in required:
            if default is ...:
                default = None
            typ = Optional[typ]
        fields[prop] = (typ, default)
    return create_model(model_name, **fields)
