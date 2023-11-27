from http import HTTPStatus
from response import CustomResponse, ERROR_CODES, ERROR_MESSAGES

from rest_framework.views import APIView
from asset_management.models import AssetService
from asset_management.serializers import AssetServiceSerializer
from rest_framework.response import Response


class AssetServiceBasicView(APIView):
    def get(self, request):
        try:
            query = request.query_params.dict()
            page = int(query['page'])
            pageSize = int(query['pageSize'])
            assetid = int(query['assetid'])
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
            resall = AssetService.objects.filter(asset_id=assetid)
            reschosen = []
            for i in resall:
                if ((str(i.id).find(content) != -1)
                        or (str(i.asset_id).find(content) != -1)
                        or (i.ip.find(content) != -1)
                        or (str(i.port).find(content) != -1)
                        or (i.name.find(content) != -1)
                        or (i.state.find(content) != -1)
                        or (i.product.find(content) != -1)
                        or (i.version.find(content) != -1)
                        or (i.cpe.find(content) != -1)
                        or (i.extrainfo.find(content) != -1)
                        or (i.update_time.find(content) != -1)):
                    reschosen.append(i)
            resdata = reschosen[(page - 1) * pageSize: page * pageSize]
            print(resdata)
            ser = AssetServiceSerializer(instance=resdata, many=True)
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
            assetservice_toadd = AssetServiceSerializer(data=request.data)
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['BAD_REQUEST'],
                msg=ERROR_MESSAGES['BAD_REQUEST'],
                data={},
                status=HTTPStatus.BAD_REQUEST
            )
        if not assetservice_toadd.is_valid():
            return CustomResponse(
                code=ERROR_CODES['BAD_REQUEST'],
                msg=ERROR_MESSAGES['BAD_REQUEST'],
                data={},
                status=HTTPStatus.BAD_REQUEST
            )
        assetservice_toadd.save()
        return CustomResponse(
            data=assetservice_toadd.data
        )

    def put(self, request):
        try:
            query = request.query_params.dict()
            pick = int(query['alternum'])
            assetservice_chosen = AssetService.objects.get(pk=pick)
            ser = AssetServiceSerializer(instance=assetservice_chosen, data=request.data)
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
            AssetService.objects.get(pk=pick).delete()
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
