from rest_framework.exceptions import APIException
from rest_framework import status


class BadRequest400(APIException):
    '''
    Raises bad request api exception error
    '''

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid request body or missing "value" field'

class NotFound404(APIException):
    '''
    Raises not found api exception error
    '''

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'String does not exist in the system'

class Conflict409(APIException):
    '''
    Raises conflit api exception error
    '''

    status_code = status.HTTP_409_CONFLICT
    default_detail = 'String already exists in the system'

class UnprocessableEntity422(APIException):
    '''
    Raises unprocessable api exception error 
    '''

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = 'Invalid data type for "value" (must be string)'

class CustomException400(APIException):
    '''
    Raises bad request api exception error with
    a different detail message
    '''

    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)

class CustomException422(APIException):
    '''
    Raises unprocessable api exception
    error with a different detail message
    '''
    
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)


