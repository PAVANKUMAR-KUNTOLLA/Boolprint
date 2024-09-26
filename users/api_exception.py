import logging

from rest_framework.exceptions import APIException
from rest_framework import status, response
from rest_framework.response import Response

from rest_framework.views import exception_handler


def generic_middleware_exception(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if not response:
        data = {"message": "Error:  " + str(exc), "status_flag": False, "status": 403, "data": {}}
        print(data)
        return Response(data, status=403)

    return response


def standard_response(data=dict(), message="Done", status_flag=True, status_num=200, status_code=status.HTTP_200_OK):
    response_text = {
        'data': data,
        'status_flag': status_flag,
        'status': status_num,
        'message': message
    }
    return response.Response(status=status_code, data=response_text)


def success_response(data=dict(), message="Success"):
    response_text = {
        'data': data,
        'status_flag': True,
        'status': 200,
        'message': message
    }
    return response.Response(status=status.HTTP_200_OK, data=response_text)


class GenericException(APIException):
    """
    raises API exceptions with custom messages and custom status codes
    """
    status_code = status.HTTP_400_BAD_REQUEST
    detail = {
        "data": {},
        "status_flag": False,
        "status": 400,
        'message': 'Error : '

    }

    def __init__(self, error_message=None, status=None, status_code=None):
        if error_message is not None:
            # self.detail["message"] = self.detail["message"] + error_message
            self.detail["message"] = 'Error : ' + error_message

        if status is not None:
            self.detail["status"] = status

        if status_code is not None:
            self.status_code = status_code

        logging.error(f"Application Generic Exception -- Status {self.detail['status']} - Message {self.detail['message']}")


class UserActiveException(APIException):
    """
    raises API exceptions with custom messages and custom status codes
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = {
        "data": {},
        "status_flag": False,
        "status": 401,
        'message': 'User in InActive'

    }

    def __init__(self, error_message=None, status=None, status_code=None):
        if error_message is not None:
            self.detail["message"] = error_message

        if status is not None:
            self.detail["status"] = status

        if status_code is not None:
            self.status_code = status_code

        # super().__init__(self.detail, self.status_code)

        logging.error(f"Application Generic User Activity Exception -- Status {self.detail['status']} - Message {self.detail['message']}")


class UserFeatureException(APIException):
    """
    raises API exceptions with custom messages and custom status codes
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = {
        "data": {},
        "status_flag": False,
        "status": 401,
        'message': 'User is not authorized for this feature'

    }

    def __init__(self, error_message=None, status=None, status_code=None):
        if error_message is not None:
            self.detail["message"] = error_message

        if status is not None:
            self.detail["status"] = status

        if status_code is not None:
            self.status_code = status_code

        logging.error(f"Application Generic User Feature Exception -- Status {self.detail['status']} - Message {self.detail['message']}")
