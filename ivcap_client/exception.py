#
# Copyright (c) 2023-2025 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
class NotAuthorizedException(Exception):
    pass

class ResourceNotFound(Exception):
    """Exception raised when requestred resource is not found.

    Attributes:
        resource -- name or URN of missing resource
    """
    def __init__(self, resource: str):
        self.resource = resource
        self.message = f"resource '{resource}' not found"
        super().__init__(self.message)

class AmbiguousRequest(Exception):
    """Exception raised when request is not specific enough.

    Attributes:
        message -- cause for ambiguity
    """
    def __init__(self, message: str):
        super().__init__(message)

class MissingParameterValue(Exception):
    pass

class HttpException(Exception):
    status_code: int
    msg: str
