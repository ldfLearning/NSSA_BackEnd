from rest_framework.response import Response

ERROR_CODES = {
    'INVALID_DATA': 1001,
    'AUTHENTICATION_FAILED': 1002,
    'PERMISSION_DENIED': 1003,
    # 其他错误码定义...
    'INVALID_REQUEST': 1004,
    'PREDICTION_ERROR': 1005,
    'DATABASE_ERROR': 1006,
    'BAD_REQUEST': 1007,
    'INTERNAL_SERVER_ERROR': 1008,
    'NOT_ACCEPTABLE': 1009,
    'PRECONDITION_FAILED': 1010,
}

ERROR_MESSAGES = {
    'INVALID_DATA': 'Invalid data',
    'AUTHENTICATION_FAILED': 'Authentication failed',
    'PERMISSION_DENIED': 'Permission denied',
    # 其他错误信息定义...
    'INVALID_REQUEST': 'Invalid request',
    'PREDICTION_ERROR': 'Situation Prediction error',
    'DATABASE_ERROR': 'Database error',
    'BAD_REQUEST': 'Bad request',
    'INTERNAL_SERVER_ERROR': 'Internal server error',
    'NOT_ACCEPTABLE': 'Not acceptable',
    'PRECONDITION_FAILED': 'Precondition failed',
}


class CustomResponse(Response):
    def __init__(self, code=0, msg='success', data=None, status=None,
                 template_name=None, headers=None, exception=False, content_type=None):
        content = {
            'code': code,
            'msg': msg,
            'data': data
        }
        super().__init__(content, status, template_name, headers, exception, content_type)