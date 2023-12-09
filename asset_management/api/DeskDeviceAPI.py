import json
import string
from datetime import datetime
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from http import HTTPStatus
from response import CustomResponse, ERROR_CODES, ERROR_MESSAGES

from asset_management.models import *
from rest_framework.response import Response

class DeskDeviceAPIView(APIView):

    def post(self, request):
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
            return CustomResponse(
                code=ERROR_CODES['BAD_REQUEST'],
                msg=ERROR_MESSAGES['BAD_REQUEST'],
                data={},
                status=HTTPStatus.BAD_REQUEST
            )
        return CustomResponse(
            data={}
        )