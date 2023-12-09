from http import HTTPStatus
from response import CustomResponse, ERROR_CODES, ERROR_MESSAGES

from rest_framework.views import APIView
from asset_management.models import *
from asset_management.serializers import ProductionlineSerializer
from rest_framework.response import Response


class ProductionlineBasicView(APIView):
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
            resall = Productionline.objects.all()
            reschosen = []
            for i in resall:
                if ((str(i.id).find(content) != -1)
                        or (i.name.find(content) != -1)
                        or (str(i.workshop_id).find(content) != -1)
                        or (i.shortened.find(content) != -1)
                        or (str(i.asset_number).find(content) != -1)):
                    reschosen.append(i)
            resdata = reschosen[(page - 1) * pageSize: page * pageSize]
            print(resdata)
            ser = ProductionlineSerializer(instance=resdata, many=True)
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
            productionline_toadd = ProductionlineSerializer(data=request.data)
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['BAD_REQUEST'],
                msg=ERROR_MESSAGES['BAD_REQUEST'],
                data={},
                status=HTTPStatus.BAD_REQUEST
            )
        if not productionline_toadd.is_valid():
            return CustomResponse(
                code=ERROR_CODES['BAD_REQUEST'],
                msg=ERROR_MESSAGES['BAD_REQUEST'],
                data={},
                status=HTTPStatus.BAD_REQUEST
            )
        productionline_toadd.save()
        return CustomResponse(
            data=productionline_toadd.data
        )

    def put(self, request):
        try:
            query = request.query_params.dict()
            pick = int(query['alternum'])
            productionline_chosen = Productionline.objects.get(pk=pick)
            ser = ProductionlineSerializer(instance=productionline_chosen, data=request.data)
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
            Productionline.objects.get(pk=pick).delete()
            assetList = Asset.objects.filter(productionline_id=pick)
            for asset in assetList:
                asset.productionline_id = 0
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