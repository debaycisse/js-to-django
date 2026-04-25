from rest_framework.views import exception_handler

def custom_exception_handler(exception, context):
    '''
    Handles exception, based on the value field
    validation failure
    '''
    output = exception_handler(
        exception, context
    )

    if hasattr(exception, 'status_code') and output is not None:
        output.status_code = exception.status_code
    return output
