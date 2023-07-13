class NotAuthorizedException(BaseException):
    pass

class ResourceNotFound(BaseException):
    pass

class MissingParameterValue(Exception):
    pass

class HttpException(Exception):
    status_code: int
    msg: str

