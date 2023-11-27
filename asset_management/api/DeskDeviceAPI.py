import json
import string
from datetime import datetime
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from asset_management.models import *

class DeskDeviceAPIView(APIView):

    def post(self, request):
        res = {'code': 0, 'msg': '远程数据库资产-本地更新成功'}
        try:
            assetdeviceinfos = AssetDeviceInfo.objects.all()
            for assetdeviceinfo in assetdeviceinfos:
                asset_list = Asset.objects.filter(ip=assetdeviceinfo.ip)
                if len(asset_list) != 0:
                    asset = asset_list[0]
                    asset.device_sn = assetdeviceinfo.device_sn
                    asset.save()
                    deskdevice_list = DeskDevice.objects.filter(sn=asset.device_sn)
                    if len(deskdevice_list) != 0:
                        deskdevice = deskdevice_list[0]
                        asset.device_type = deskdevice.device_type
                        asset.save()
        except Exception as e:
            res['code'] = -1
            res['msg'] = '远程数据库资产-本地更新失败'
        return JsonResponse(res)