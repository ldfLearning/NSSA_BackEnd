import xlrd
import xlwt
from rest_framework import status
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from asset_management.models import *

from asset_management.file import fileOut


# 本文件中的函数负责单位部门的文件导出和导入
class ProductionlineFileView(APIView):
    def get(self, request):  # 从数据库取出信息，返回到前端
        res = {'code': 0, 'msg': '导出成功'}
        try:
            return productionlineFileOut()
        except Exception as e:
            print(repr(e))
            res['code'] = 1
            res['msg'] = '导出失败'
            return JsonResponse(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):  # 处理前端发送过来的post请求，包含增删改查等多种类型
        res = {'code': 0, 'msg': '导入成功'}
        print(f"req: {request} file: {request.FILES}")
        try:
            file_object = request.FILES['file']
            if file_object:
                print("get file")
                return productionlineFileIn(file_object)
            else:
                res['code'] = 1
                res['msg'] = '文件打开失败'
                return JsonResponse(res, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            res['code'] = 2
            res['msg'] = '文件导入失败'
            return JsonResponse(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def productionlineFileOut():  # 将数据库中的主机信息导出到excel文件
    # 表头内容
    columns = ['ID', '产线名称', '产线简称', '所属车间ID', '资产数量']
    # 获取数据库数据
    rows = Productionline.objects.all().values_list('id', 'name', 'shortened', 'workshop_id', 'asset_number')
    return fileOut(columns, rows, 'Productionline')


# 导入的表要和导出的表格式一致，即都需要在第一列加上ID，但是导入表中的ID不重要，因为只会从第二列开始读取数据，数据库中的ID会自动生成
def productionlineFileIn(f):
    res = {'code': 0, 'msg': '导入成功'}
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
                    productionlineList = Productionline.objects.filter(name=rowValues[1])
                    if len(productionlineList) == 0:  # 如果数据库中不存在单位名，新创建一条主机信息
                        productionline = Productionline(name=rowValues[1], shortened=rowValues[2],
                                                        workshop_id=rowValues[3], asset_number=rowValues[4])
                    else:  # 如果已经存在,则更新字段值
                        productionline = Productionline.objects.get(name=rowValues[1])
                        productionline.shortened = rowValues[2]
                        productionline.workshop_id = rowValues[3]
                        productionline.asset_number = rowValues[4]
                    productionline.save()
        except Exception as e:
            print(e)
            res['code'] = 3
            res['msg'] = '导入过程出现错误....'
            return JsonResponse(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JsonResponse(res)
    res['code'] = 2
    res['msg'] = '上传文件格式不是xlsx'
    return JsonResponse(res, status=status.HTTP_412_PRECONDITION_FAILED)
