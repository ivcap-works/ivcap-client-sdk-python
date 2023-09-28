#
# Copyright (c) 2023 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
class NotAuthorizedException(BaseException):
    pass

class ResourceNotFound(BaseException):
    pass

class MissingParameterValue(Exception):
    pass

class HttpException(Exception):
    status_code: int
    msg: str

