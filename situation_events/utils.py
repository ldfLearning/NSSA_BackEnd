from django.http import JsonResponse
from django.db import connection


class HttpCode(object):
    # 成功
    ok = 200
    # 服务器内部错误
    error = 500
    # 未找到数据库字段
    not_found = 400


def result(code=HttpCode.ok, message="", data=[], total=0, count=0):
    if code == HttpCode.ok:
        code = 0
    res = {"code": code, "msg": message, "data": data, "total": total, "count": count}
    return JsonResponse(res)

