from rest_framework.views import exception_handler
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

        if response.status_code == status.HTTP_404_NOT_FOUND:
            response.data['message'] = 'The requested resource was not found.'
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            response.data['message'] = 'There was an error with your request. Please check your input and try again.'
        else:
            response.data['message'] = 'An unexpected error occurred.'

    return response
