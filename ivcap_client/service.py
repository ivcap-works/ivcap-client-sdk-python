#
# Copyright (c) 2023-2025 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
from __future__ import annotations # postpone evaluation of annotations
import asyncio
import io
import json
from typing import IO, TYPE_CHECKING, Awaitable, Dict, List, Optional, Any, List, Optional, Dict, Set, Union

from httpx import Response
from pydantic import BaseModel

if TYPE_CHECKING:
    from ivcap_client.ivcap import IVCAP, URN
    from ivcap_client.job import Job

import datetime
from dataclasses import asdict, dataclass, field, is_dataclass
from enum import Enum

from ivcap_client.api.service import service_service_list, service_service_read

from ivcap_client.models.parameter_def_t import ParameterDefT
from ivcap_client.models.parameter_opt_t import ParameterOptT
from ivcap_client.models.service_list_item_t import ServiceListItemT
from ivcap_client.models.service_list_rt import ServiceListRT
from ivcap_client.models.service_status_rt import ServiceStatusRT
from ivcap_client.models.service_status_rt_status import ServiceStatusRTStatus

from ivcap_client.utils import BaseIter, Links, _set_fields, _unset, _unset_bool, model_from_json_schema, process_error

@dataclass
class Service:
    """This class represents a particular service available
    in a particular IVCAP deployment"""

    id: Optional[URN] = None
    name: Optional[str] = None
    description: Optional[str] = None
    banner: Optional[str] = None


    policy: Optional[URN] = None
    published_at: Optional[datetime.datetime] = None
    policy: Optional[URN] = None
    account: Optional[URN] = None


    @classmethod
    def _from_list_item(cls, item: ServiceListItemT, ivcap: IVCAP):
        kwargs = item.to_dict()
        return cls(ivcap, **kwargs)

    def __init__(self, ivcap: IVCAP, **kwargs):
        if not ivcap:
            raise ValueError("missing 'ivcap' argument")
        self._ivcap = ivcap
        self._request_model = None
        self.__update__(**kwargs)

    def __update__(self, **kwargs):
        p = ["id", "name", "description", "banner", "policy", "published-at", "account"]
        hp = ["status"]
        _set_fields(self, p, hp, kwargs)

        self._parameters: Optional[dict[str, ServiceParameter]] = None
        params = kwargs.get("parameters")
        if params != None:
            pd = dict(map(lambda d: [d["name"].replace('-', '_'), ServiceParameter(ParameterDefT.from_dict(d))], params))
            self._parameters = pd

    def status(self, refresh = True) -> ServiceStatusRTStatus:
        if refresh:
            self.refresh()
        return self._status

    @property
    def parameters(self) -> Dict[str, ServiceParameter]:
        if not self._parameters:
            self.refresh()
        return self._parameters

    @property
    def mandatory_parameters(self) -> Set[str]:
        v = self.parameters.values()
        f = map(lambda p: p.name, filter(lambda p: not p.is_optional, v))
        return set(f)

    @property
    def request_model(self) -> type[BaseModel]:
        if not self._request_model:
            return self._fetch_request_model()
        return self._request_model

    def _fetch_request_model(self) -> type[BaseModel]:
        if not self._request_model:
            schema = 'urn:sd-core:schema.ai-tool.1'
            l = self._ivcap.list_aspects(schema=schema, entity=self.id, include_content=False, limit=2)
            if not l.has_next():
                raise ValueError("cannot find request (tool) model for this service")
            m = next(l)
            if l.has_next():
                raise OverflowError(f"Found more then one model definition")
            js = m.aspect["fn_schema"]
            self._request_model = model_from_json_schema(js, f"Service{id(self)}")
        return self._request_model

    async def request_model_async(self) -> Awaitable[type[BaseModel]]:
        if self._request_model:
            return self._request_model
        return await asyncio.to_thread(self._fetch_request_model)

    def request_job(self, data: Union[BaseModel, object, IO[str]], timeout:Optional[int]=0) -> Job:
        kwargs = self._get_request_job_args(data, timeout)
        response = self._ivcap._client.get_httpx_client().request(**kwargs)
        return self._process_job_reply(response)

    async def request_job_async(self, data: Union[BaseModel, object, IO[str]], timeout:Optional[int]=0) -> Awaitable[Job]:
        kwargs = self._get_request_job_args(data, timeout)
        response = await self._ivcap._client.get_async_httpx_client().request(**kwargs)
        return self._process_job_reply(response)

    def _get_request_job_args(self, data: Union[BaseModel, object, IO[str]], timeout:Optional[int]=0):
        headers: dict[str, Any] = {
            "Timeout": str(timeout if timeout != None else 0),
            "Content-Type": "application/json",
        }
        kwargs: dict[str, Any] = {
            "method": "post",
            "url": f"/1/services2/{self.id}/jobs",
        }

        # serialise 'data' into a json object
        if isinstance(data, io.IOBase) and hasattr(data, 'read') and callable(data.read):
            try:
                # Attempt to load JSON from the file object
                loaded_body = json.load(data)
                body = json.dumps(loaded_body, indent=2)
            except json.JSONDecodeError:
                raise ValueError("The provided file object does not contain valid JSON.")
        elif is_dataclass(data):
            body = json.dumps(asdict(data), indent=2)
        elif isinstance(data, BaseModel):
            body = data.model_dump_json(indent=2)
        else:
            raise TypeError(
                "Input data must be a dataclass object, Pydantic instance, "
                "or a readable file object containing JSON."
            )

        kwargs["data"] = body
        kwargs["headers"] = headers
        return kwargs

    def _process_job_reply(self, response: Response) -> Job:
        if response.status_code >= 300:
            return process_error('request_job', response)

        from ivcap_client.job import Job
        return Job.from_create_job_response(response, self)

    def refresh(self) -> Service:
        r = service_service_read.sync_detailed(self.id, client=self._ivcap._client)
        if r.status_code >= 300:
            return process_error('create_service', r)

        p: ServiceStatusRT = r.parsed
        self.__update__(**p.to_dict())
        return self

    def __repr__(self):
        name = self.name if self.name else "???"
        return f"<Service id={self.id}, name={name}>"

class ServiceIter(BaseIter[Service, ServiceListItemT]):
    def __init__(self, ivcap: 'IVCAP', **kwargs):
        super().__init__(ivcap, **kwargs)

    def _next_el(self, el) -> Service:
        return Service._from_list_item(el, self._ivcap)

    def _get_list(self) -> List[ServiceListItemT]:
        r = service_service_list.sync_detailed(**self._kwargs)
        if r.status_code >= 300 :
            return process_error('service_list', r)
        l: ServiceListRT = r.parsed
        self._links = Links(l.links)
        return l.items

class PType(Enum):
    STRING = 'string'
    INT = 'int'
    FLOAT = 'float'
    BOOL = 'bool'
    OPTION = 'option'
    ARTIFACT = 'artifact'
    COLLECTION = 'collection'

_verifier = {
    PType.STRING: lambda v, s: isinstance(v, str),
    PType.INT: lambda v, s: isinstance(v, int),
    PType.FLOAT: lambda v, s: isinstance(v, float),
    PType.BOOL: lambda v, s: isinstance(v, bool),
    PType.OPTION: lambda v, s: s._verify_option(v),
    PType.ARTIFACT: lambda v, s: s._verify_artifact(v),
    PType.COLLECTION: lambda v, s: s._verify_collection(v),
}

@dataclass(init=False)
class ServiceParameter:
    name: str
    type: PType
    description: str
    label: Optional[str] = None
    unit: Optional[str] = None
    is_constant: Optional[bool] = False
    is_unary: Optional[bool] = False
    is_optional: Optional[bool] = False
    default: Optional[str] = None
    options: Optional[List["ParameterOptT"]] = field(default_factory=list)

    def __init__(self, p: ParameterDefT):
        self.name = p.name
        self.type = PType(p.type)
        self.description = p.description
        self.label = _unset(p.label)
        self.unit = _unset(p.unit)
        self.is_constant = _unset_bool(p.constant)
        self.is_unary = _unset_bool(p.unary)
        self.default = _unset(p.default)
        self.options = list(map(POption, _unset(p.options)))

        # HACK: API is providing wrong information
        optional = _unset_bool(p.optional)
        if not optional and self.default != None:
            optional = True
        self.is_optional = optional

    def verify(self, value: Any):
        """Verify if value is within the constraints and types defined
        for this parameter"""
        if not _verifier[self.type](value, self):
            raise Exception(f"value '{type(value)}:{self.type}' is not a valid for parameter {self}")

    def _verify_option(self, value: Any) -> bool:
        print(f"=====verify '{value}' {self.name}: {self.options}")
        l = list(filter(lambda o: o.value == value, self.options))
        return len(l) > 0

    def _verify_artifact(self, v: Any) -> bool:
        if not isinstance(v, str):
            return False
        if v.startswith("urn:ivcap:artifact:"):
            return True
        if v.startswith("https://") or v.startswith("http://"):
            return True
        if v.startswith("urn:https://") or v.startswith("urn:http://"):
            return True
        return False

    def _verify_collection(self, v: Any) -> bool:
        if not isinstance(v, str):
            return False
        if v.startswith("urn:"):
            return True
        return False

    def __repr__(self):
        return f"<Parameter name={self.name}, type={self.type.name} is_optional={self.is_optional}>"

@dataclass(init=False)
class POption:
    value: str
    description: Optional[str] = None

    def __init__(self, p: ParameterOptT):
        self.value = p.value
        self.description = _unset(p.description)

    def __repr__(self):
        return f"<Option value={self.value}>"
