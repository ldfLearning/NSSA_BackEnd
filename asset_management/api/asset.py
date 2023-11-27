from http import HTTPStatus
from response import CustomResponse, ERROR_CODES, ERROR_MESSAGES

from rest_framework.views import APIView
from asset_management.models import *
from asset_management.serializers import AssetSerializer
from rest_framework.response import Response


class AssetBasicView(APIView):

    def get(self, request):
        try:
            query = request.query_params.dict()
            page = int(query['page'])
            pageSize = int(query['pageSize'])
            content = str(query['content'])
        except Exception as e:
            print(e)
            return CustomResponse(
                code=ERROR_CODES['BAD_REQUEST'],
                msg=ERROR_MESSAGES['BAD_REQUEST'],
                data={},
                status=HTTPStatus.BAD_REQUEST
            )
        try:
            resall = Asset.objects.all()
            reschosen = []
            for i in resall:
                if ((str(i.id).find(content) != -1)
                        or (i.ip.find(content) != -1)
                        or (i.name.find(content) != -1)
                        or (i.position.find(content) != -1)
                        or (i.device_sn.find(content) != -1)
                        or (i.device_vendor.find(content) != -1)
                        or (i.device_type.find(content) != -1)
                        or (i.device_working_hours.find(content) != -1)
                        or (str(i.cpu_used).find(content) != -1)
                        or (str(i.remain_mem).find(content) != -1)
                        or (str(i.remain_harddisk).find(content) != -1)
                        or (str(i.network_speed).find(content) != -1)
                        or (i.os.find(content) != -1)
                        or (i.mac.find(content) != -1)
                        or (i.update_time.find(content) != -1)
                        or (str(i.productionline_id).find(content) != -1)):
                    reschosen.append(i)
            resdata = reschosen[(page - 1) * pageSize: page * pageSize]
            print(resdata)
            ser = AssetSerializer(instance=resdata, many=True)
            total = len(reschosen)
            totalPage = total // pageSize + 1
        except Exception as e:
            print(e)
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=ERROR_MESSAGES['INTERNAL_SERVER_ERROR'],
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        data = {'total': total, 'totalPage': totalPage, 'nowPage': page, 'list': ser.data}
        return CustomResponse(
            data=data
        )

    def post(self, request):
        try:
            asset_toadd = AssetSerializer(data=request.data)
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['BAD_REQUEST'],
                msg=ERROR_MESSAGES['BAD_REQUEST'],
                data={},
                status=HTTPStatus.BAD_REQUEST
            )
        if not asset_toadd.is_valid():
            return CustomResponse(
                code=ERROR_CODES['BAD_REQUEST'],
                msg=ERROR_MESSAGES['BAD_REQUEST'],
                data={},
                status=HTTPStatus.BAD_REQUEST
            )
        asset_toadd.save()
        return CustomResponse(
            data=asset_toadd.data
        )

    def put(self, request):
        try:
            query = request.query_params.dict()
            pick = int(query['alternum'])
            asset_chosen = Asset.objects.get(pk=pick)
            ser = AssetSerializer(instance=asset_chosen, data=request.data)
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['BAD_REQUEST'],
                msg=ERROR_MESSAGES['BAD_REQUEST'],
                data={},
                status=HTTPStatus.BAD_REQUEST
            )
        if not ser.is_valid():
            return CustomResponse(
                code=ERROR_CODES['BAD_REQUEST'],
                msg=ERROR_MESSAGES['BAD_REQUEST'],
                data={},
                status=HTTPStatus.BAD_REQUEST
            )
        ser.save()
        return CustomResponse(
            data=ser.data
        )

    def delete(self, request):
        try:
            query = request.query_params.dict()
            pick = int(query['deletenum'])
            Asset.objects.get(pk=pick).delete()
            serviceList = AssetService.objects.filter(asset_id=pick)
            print(serviceList)
            for service in serviceList:
                service.delete()
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
