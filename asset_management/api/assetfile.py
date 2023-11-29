from http import HTTPStatus
from response import CustomResponse, ERROR_CODES, ERROR_MESSAGES

import xlrd
import xlwt
from rest_framework import status
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from asset_management.models import *

from asset_management.file import fileOut


# 本文件中的函数负责单位部门的文件导出和导入
class AssetFileView(APIView):
    def get(self, request):  # 从数据库取出信息，返回到前端
        res = {'code': 0, 'msg': '导出成功'}
        try:
            return assetFileOut()
        except Exception as e:
            # 导出失败
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=ERROR_MESSAGES['INTERNAL_SERVER_ERROR'],
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    def post(self, request):  # 处理前端发送过来的post请求，包含增删改查等多种类型
        res = {'code': 0, 'msg': '导入成功'}
        print(f"req: {request} file: {request.FILES}")
        try:
            file_object = request.FILES['file']
            if file_object:
                print("get file")
                return assetFileIn(file_object)
            else:
                # 文件打开失败
                return CustomResponse(
                    code=ERROR_CODES['NOT_ACCEPTABLE'],
                    msg=ERROR_MESSAGES['NOT_ACCEPTABLE'],
                    data={},
                    status=HTTPStatus.NOT_ACCEPTABLE
                )
        except Exception as e:
            # 文件导入失败
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=ERROR_MESSAGES['INTERNAL_SERVER_ERROR'],
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )


def assetFileOut():  # 将数据库中的主机信息导出到excel文件
    # 表头内容
    columns = ['ID', '资产IP', '资产名称', '位置', '设备SN', '设备厂商', '设备类型', '设备工作时长', 'CPU使用率', '剩余内存空间',
               '剩余硬盘空间', '网速', '操作系统', 'MAC地址', '更新时间', '所属产线ID']
    # 获取数据库数据
    rows = Asset.objects.all().values_list('id', 'ip', 'name', 'position', 'device_sn', 'device_vendor', 'device_type',
                                           'device_working_hours', 'cpu_used', 'remain_mem', 'remain_harddisk',
                                           'network_speed', 'os', 'mac', 'update_time', 'productionline_id')
    return fileOut(columns, rows, 'Asset')


# 导入的表要和导出的表格式一致，即都需要在第一列加上ID，但是导入表中的ID不重要，因为只会从第二列开始读取数据，数据库中的ID会自动生成
def assetFileIn(f):
    type_excel = f.name.split('.')[1]
    if type_excel in ['xlsx', 'xls']:  # 支持的文件格式
        # 开始解析上传的excel表格
        wb = xlrd.open_workbook(filename=None, file_contents=f.read())  # 关键点在于这里
        table = wb.sheets()[0]
        nrows = table.nrows  # 行数
        try:
            with transaction.atomic():
                for i in range(1, nrows):  # 从1开始是为了去掉表头
                    rowValues = table.row_values(i)  # 一行的数据
                    assetList = Asset.objects.filter(ip=rowValues[1])
                    if len(assetList) == 0:  # 如果数据库中不存在单位名，新创建一条主机信息
                        asset = Asset(ip=rowValues[1], name=rowValues[2], position=rowValues[3], device_sn=rowValues[4],
                                      device_vendor=rowValues[5], device_type=rowValues[6],
                                      device_working_hours=rowValues[7], cpu_used=rowValues[8],
                                      remain_mem=rowValues[9], remain_harddisk=rowValues[10],
                                      network_speed=rowValues[11], os=rowValues[12], mac=rowValues[13],
                                      update_time=rowValues[14], productionline_id=rowValues[15])
                    else:  # 如果已经存在,则更新字段值
                        asset = Asset.objects.get(ip=rowValues[1])
                        asset.name = rowValues[2]
                        asset.position = rowValues[3]
                        asset.device_sn = rowValues[4]
                        asset.device_vendor = rowValues[5]
                        asset.device_type = rowValues[6]
                        asset.device_working_hours = rowValues[7]
                        asset.cpu_used = rowValues[8]
                        asset.remain_mem = rowValues[9]
                        asset.remain_harddisk = rowValues[10]
                        asset.network_speed = rowValues[11]
                        asset.os = rowValues[12]
                        asset.mac = rowValues[13]
                        asset.update_time = rowValues[14]
                        asset.productionline_id = rowValues[15]
                    asset.save()
        except Exception as e:
            print(e)
            # 导入过程出现错误
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=ERROR_MESSAGES['INTERNAL_SERVER_ERROR'],
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        return CustomResponse(
            data={}
        )
    # 上传文件格式不是xlsx
    return CustomResponse(
        code=ERROR_CODES['PRECONDITION_FAILED'],
        msg=ERROR_MESSAGES['PRECONDITION_FAILED'],
        data={},
        status=HTTPStatus.PRECONDITION_FAILED
    )
