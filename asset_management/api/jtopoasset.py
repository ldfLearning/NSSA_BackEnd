import json

from django.core import serializers
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from asset_management.api.jtopojson import *
from asset_management.models import JtopoDevices


class JtopoAssetView(APIView):
    def get(self, request):
        res = {'code': 0, 'msg': ''}
        try:
            querySet = JtopoDevices.objects.all()
            devices = json.loads(serializers.serialize("json", querySet))
            res['data'] = devices
            res['msg'] = '获取设备数据成功'
        except Exception as e:
            res['code'] = -1
            res['msg'] = '获取设备数据失败'
        return JsonResponse(res)

    # TODO 添加设备后更新Json文件
    # 增加设备
    def post(self, request):
        data = json.loads(request.body)
        query = data['asset_json']
        res = {'code': 0, 'msg': '新增设备成功'}
        list = JtopoDevices.objects.filter(name=query['name'])
        if (len(list) > 0):
            res['code'] = -1
            res['msg'] = '同名设备已经存在'
            return JsonResponse(res, status=status.HTTP_412_PRECONDITION_FAILED)
        try:
            JtopoDevices.objects.create(name=query['name'], type=query['type'], title=query['descrip'],
                                        imgUrl=query['icon'])
            # 更新json文件中的设备列表
            filepath = "asset_management/files/static/topo.json"
            load_dict = readJson(filepath)
            load_dict["AssetList"] = generateDeviceList()
            writeJson(load_dict, filepath)
            # res['data'] = readJson(filepath)
            res['data'] = load_dict
        except Exception as e:
            res['code'] = 1
            res['msg'] = '新增设备失败'
            return JsonResponse(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JsonResponse(res)

    def delete(self, request):
        query = request.query_params.dict()
        res = {'code': 0, 'msg': '删除成功'}
        list = JtopoDevices.objects.filter(name=query['name'])
        if (len(list) == 0):
            res['code'] = -1
            res['msg'] = '无该设备'
            return JsonResponse(res, status=status.HTTP_412_PRECONDITION_FAILED)
        # print(data)
        try:
            device = JtopoDevices.objects.filter(name=query['name'])
            device.delete()
            # 更新json文件中的设备列表
            filepath = "asset_management/files/static/topo.json"
            load_dict = readJson(filepath)
            load_dict["AssetList"] = generateDeviceList()
            writeJson(load_dict, filepath)
            res['data'] = load_dict
        except Exception as e:
            res['code'] = -1
            res['msg'] = '删除失败'
            return JsonResponse(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JsonResponse(res)
