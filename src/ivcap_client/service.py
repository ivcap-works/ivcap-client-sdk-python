
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

from typing import Any, List, Optional, Dict, Set
from ivcap_client.api.order import order_create
from ivcap_client.api.service import service_list, service_read

from ivcap_client.models.order_request_t import OrderRequestT
from ivcap_client.models.order_status_rt import OrderStatusRT
from ivcap_client.models.parameter_def_t import ParameterDefT
from ivcap_client.models.parameter_opt_t import ParameterOptT
from ivcap_client.models.parameter_t import ParameterT
from ivcap_client.models.service_list_item import ServiceListItem
from ivcap_client.models.service_list_rt import ServiceListRT
from ivcap_client.models.service_status_rt import ServiceStatusRT
from ivcap_client.order import Order
from ivcap_client.utils import process_error, set_page
from ivcap_client.types import Unset

class Service:
    """This clas represents a particular service available
    in a particular IVCAP deployment"""

    def __init__(self, id: str, ivcap: 'IVCAP', listItem: Optional[ServiceListItem] = None):
        self._id = id

        self._name = _unset(listItem.name) if listItem else None
        self._description = _unset(listItem.description) if listItem else None
        self._status = None
        self._provider = _unset(listItem.provider) if listItem else None
        self._description = _unset(listItem.description) if listItem else None
        self._parameters: dict[str, ParameterDefT] = None
        self._ivcap = ivcap

    @property
    def urn(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def status(self, refresh = True) -> str:
        if refresh:
            self._refresh()
        return self._status

    @property
    def parameters(self) -> Dict[str, Parameter]:
        if not self._parameters:
            self._refresh()
        return self._parameters

    def place_order(self, **kwargs) -> Order:
        pl:list[ParameterT] = []
        mandatory = self._mandatory_parameters()
        for name, value in kwargs.items():
            p = self._parameters.get(name)
            if not p:
                raise f"Unknown parameter '{name}'"
            p.verify(value)
            mandatory.discard(name)
            pl.append(ParameterT(name=name, value=value))
        if len(mandatory) > 0:
            raise Exception(f"missing mandatory parameters '{mandatory}'")

        req = OrderRequestT(parameters=pl, 
                            service_id=self._id , 
                            account_id=self._ivcap._account_id)
        r = order_create.sync_detailed(client=self._ivcap._client, json_body=req)
        if r.status_code >= 300:
            return process_error('place_order', r)
        status:OrderStatusRT = r.parsed
        return Order(status.id, self._ivcap, status)

    def _mandatory_parameters(self) -> Set[str]: 
        v = self.parameters.values()
        f = map(lambda p: p.name, filter(lambda p: not p.is_optional, v))
        return set(f)

    def _refresh(self): 
        r = service_read.sync_detailed(self._id, client=self._ivcap._client)
        if r.status_code >= 300:
            return process_error('create_service', r)

        p: ServiceStatusRT = r.parsed
        self._name = _unset(p.name)
        self._description = _unset(p.description)
        self._status = _unset(p.status)
        self._provider = _unset(p.provider)
        self._description = _unset(p.description)
        self._parameters: dict[str, Parameter] = dict(map(lambda d: [d.name.replace('-', '_'), Parameter(d)], p.parameters))

    def __repr__(self):
        return f"<Service id={self._id}, name={self._name}>"


class ServiceIter:
    def __init__(self, ivcap: 'IVCAP', **kwargs):
        self._ivcap = ivcap
        self._kwargs = kwargs
        self._links = None # init navigation
        self._items = self._fill()

    def __iter__(self):
        return self

    def __next__(self):
        if len(self._items) == 0:
            self._items = self._fill()

        if len(self._items) == 0:
            raise StopIteration
        
        el = self._items.pop(0)
        return Service(el.id, self._ivcap, el)
        
    def _fill(self) ->  List[ServiceListItem]:
        if self._links:
            if not self._links.next_:
                return []
            else:
                self._kwargs['page'] = set_page(self._links.next_)
        r = service_list.sync_detailed(**self._kwargs)
        if r.status_code >= 300 :
            return process_error('service_list', r)
        l: ServiceListRT = r.parsed
        self._links = l.links
        return l.services

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
class Parameter:
    name: str
    type: PType
    unit: str = None
    is_constant: bool = False
    default: str = None
    description: str = None
    label: str = None
    is_optional: bool = False
    options: field(default_factory=list) # List["ParameterOptT"]] = UNSET

    def __init__(self, p: ParameterDefT):
        self.name = p.name
        self.type = PType(p.type)
        self.unit = _unset(p.unit)
        self.is_constant = _unset(p.constant)
        self.default = _unset(p.default)
        self.description = _unset(p.description)
        self.label = _unset(p.label)
        # HACK: API is providing wrong information
        optional = _unset(p.optional)
        if not optional and self.default != None:
            optional = True
        self.is_optional = optional
        self.options = list(map(POption, _unset(p.options)))

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
    description: str = None

    def __init__(self, p: ParameterOptT):
        self.value = p.value
        self.description = _unset(p.description)

    def __repr__(self):
        return f"<Option value={self.value}>"

    


def _unset(v):
    v = None if isinstance(v, Unset) else v
    if v == '':
        v = None
    return v
