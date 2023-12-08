from rest_framework.response import Response

ERROR_CODES = {
    'INVALID_DATA': 1001,
    'AUTHENTICATION_FAILED': 1002,
    'PERMISSION_DENIED': 1003,
    # 其他错误码定义...
    'INVALID_REQUEST': 1004,
    'PREDICTION_ERROR': 1005,
    'DATABASE_ERROR': 1006,

}

ERROR_MESSAGES = {
    'INVALID_DATA': 'Invalid data',
    'AUTHENTICATION_FAILED': 'Authentication failed',
    'PERMISSION_DENIED': 'Permission denied',
    # 其他错误信息定义...
    'INVALID_REQUEST': 'Invalid request',
    'PREDICTION_ERROR': 'Situation Prediction error',
    'DATABASE_ERROR': 'Database error',
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