import xlrd
import xlwt
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from asset_management.models import *
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.core.files.storage import get_storage_class
from django.core.files.base import ContentFile


def fileOut(columns, rows, tablename):  # 导出数据库内容到excel文件
    # 指定数据类型
    response = HttpResponse(content_type='application/ms-excel')
    # 设置文件名称
    tablename = tablename + 'Infos.xls'
    response['Content-Disposition'] = 'attachment; filename=' + tablename
    # 创建工作簿
    wb = xlwt.Workbook(encoding='utf-8')
    # 创建表
    ws = wb.add_sheet('Menu')
    row_num = 0
    font_style = xlwt.XFStyle()
    # 二进制
    font_style.font.bold = True
    # 写进表头内容
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    # 遍历提取出来的内容
    for row in rows:
        row_num += 1
        # 逐行写入Excel
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response