from rest_framework.exceptions import APIException


class CustomAPIException(APIException):

    def __init__(self, detail=None, code=None, error_id=None):
        super().__init__(detail=detail, code=code)
        self.error_id = error_id
        self.status_code = code
