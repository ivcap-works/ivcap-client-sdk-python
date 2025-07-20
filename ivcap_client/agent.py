#
# Copyright (c) 2023-2025 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
from __future__ import annotations # postpone evaluation of annotations
import io
import json
from time import sleep
from typing import IO, TYPE_CHECKING, Awaitable, Dict, List, Optional, Any, List, Optional, Dict, Set, Union

from pydantic import BaseModel

from ivcap_client.models.service_status_rt_status import ServiceStatusRTStatus


if TYPE_CHECKING:
    from ivcap_client.ivcap import IVCAP, URN
    from ivcap_client.job import Job
    from ivcap_client.service import Service

import datetime
from dataclasses import asdict, dataclass, field, is_dataclass
from enum import Enum

@dataclass
class Agent:
    """This class represents a particular agent available
    in a particular IVCAP deployment"""

    id: URN
    # name: Optional[str] = None
    # description: Optional[str] = None

    # service: Service

    # @classmethod
    # def _from_list_item(cls, item: AgentListItemT, ivcap: IVCAP):
    #     kwargs = item.to_dict()
    #     return cls(ivcap, **kwargs)

    def __init__(self, ivcap: IVCAP, id: URN):
        if not ivcap:
            raise ValueError("missing 'ivcap' argument")
        self._ivcap = ivcap
        self._id = id
        if id.startswith("urn:ivcap:service:"):
            self._service = ivcap.get_service(id)
        else:
            raise ValueError(f"Invalid agent ID: {id}")


    def __update__(self, **kwargs):
        pass

    def status(self, refresh = True) -> ServiceStatusRTStatus:
        if refresh:
            self.refresh()
        return self._status

    @property
    def request_model(self) -> type[BaseModel]:
        return self._service.request_model

    async def request_model_async(self) -> Awaitable[type[BaseModel]]:
        return self._service.request_model_async

    # def request_job(self, data: Union[BaseModel, object, IO[str]], timeout:Optional[int]=0) -> Job:
    #     return self._service.request_job(data, timeout)

    # async def request_job_async(self, data: Union[BaseModel, object, IO[str]], timeout:Optional[int]=0) -> Awaitable[Job]:
    #     return self._service.request_job_async(data, timeout)

    def exec_agent(self, data: Union[BaseModel, object, IO[str]], timeout:Optional[int]=0) -> Job:
        """Executes the agent with the given data and returns a Job object."""
        wait_until_done = timeout == 0
        job = self._service.request_job(data, timeout)
        if wait_until_done:
            while not job.finished:
                sleep(3)
        return job

    def __repr__(self):
        name = self.name if self.name else "???"
        return f"<Agent id={self.id}, name={name}>"

# class AgentIter(BaseIter[Agent, AgentListItemT]):
#     def __init__(self, ivcap: 'IVCAP', **kwargs):
#         super().__init__(ivcap, **kwargs)

#     def _next_el(self, el) -> Agent:
#         return Agent._from_list_item(el, self._ivcap)

#     def _get_list(self) -> List[AgentListItemT]:
#         r = agent_agent_list.sync_detailed(**self._kwargs)
#         if r.status_code >= 300 :
#             return process_error('agent_list', r)
#         l: AgentListRT = r.parsed
#         self._links = Links(l.links)
#         return l.items
