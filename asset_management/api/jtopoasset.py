import json

from django.core import serializers
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from http import HTTPStatus
from response import CustomResponse, ERROR_CODES, ERROR_MESSAGES

from asset_management.api.jtopojson import *
from asset_management.models import JtopoDevices
from rest_framework.response import Response

class JtopoAssetView(APIView):
    def get(self, request):
        try:
            querySet = JtopoDevices.objects.all()
            devices = json.loads(serializers.serialize("json", querySet))
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['BAD_REQUEST'],
                msg=ERROR_MESSAGES['BAD_REQUEST'],
                data={},
                status=HTTPStatus.BAD_REQUEST
            )
        return CustomResponse(
            data=devices
        )

    # TODO 添加设备后更新Json文件
    # 增加设备
    def post(self, request):
        data = json.loads(request.body)
        query = data['asset_json']
        list = JtopoDevices.objects.filter(name=query['name'])
        if (len(list) > 0):
            # 同名设备已经存在
            return CustomResponse(
                code=ERROR_CODES['PRECONDITION_FAILED'],
                msg=ERROR_MESSAGES['PRECONDITION_FAILED'],
                data={},
                status=HTTPStatus.PRECONDITION_FAILED
            )
        try:
            JtopoDevices.objects.create(name=query['name'], type=query['type'], title=query['descrip'],
                                        imgUrl=query['icon'])
            # 更新json文件中的设备列表
            filepath = "asset_management/files/jtopo_json/topo.json"
            load_dict = readJson(filepath)
            load_dict["AssetList"] = generateDeviceList()
            writeJson(load_dict, filepath)
            # res['data'] = readJson(filepath)
            # res['data'] = load_dict
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        return CustomResponse(
            data=load_dict
        )

    def delete(self, request):
        query = request.query_params.dict()
        list = JtopoDevices.objects.filter(name=query['name'])
        if (len(list) == 0):
            # 无该设备
            return CustomResponse(
                code=ERROR_CODES['PRECONDITION_FAILED'],
                msg=ERROR_MESSAGES['PRECONDITION_FAILED'],
                data={},
                status=HTTPStatus.PRECONDITION_FAILED
            )
        # print(data)
        try:
            device = JtopoDevices.objects.filter(name=query['name'])
            device.delete()
            # 更新json文件中的设备列表
            filepath = "asset_management/files/jtopo_json/topo.json"
            load_dict = readJson(filepath)
            load_dict["AssetList"] = generateDeviceList()
            writeJson(load_dict, filepath)
            # res['data'] = load_dict
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        return CustomResponse(
            data=load_dict
        )
