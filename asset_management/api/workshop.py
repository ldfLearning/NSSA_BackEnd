from http import HTTPStatus
from response import CustomResponse, ERROR_CODES, ERROR_MESSAGES

from rest_framework.views import APIView
from asset_management.models import *
from asset_management.serializers import WorkshopSerializer
from rest_framework.response import Response


class WorkshopBasicView(APIView):

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
            resall = Workshop.objects.all()
            reschosen = []
            for i in resall:
                if ((str(i.id).find(content) != -1)
                        or (i.name.find(content) != -1)
                        or (i.shortened.find(content) != -1)
                        or (str(i.productionline_number).find(content) != -1)):
                    reschosen.append(i)
            resdata = reschosen[(page - 1) * pageSize: page * pageSize]
            print(resdata)
            ser = WorkshopSerializer(instance=resdata, many=True)
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
            workshop_toadd = WorkshopSerializer(data=request.data)
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['BAD_REQUEST'],
                msg=ERROR_MESSAGES['BAD_REQUEST'],
                data={},
                status=HTTPStatus.BAD_REQUEST
            )
        if not workshop_toadd.is_valid():
            return CustomResponse(
                code=ERROR_CODES['BAD_REQUEST'],
                msg=ERROR_MESSAGES['BAD_REQUEST'],
                data={},
                status=HTTPStatus.BAD_REQUEST
            )
        workshop_toadd.save()
        return CustomResponse(
            data=workshop_toadd.data
        )

    def put(self, request):
        try:
            query = request.query_params.dict()
            pick = int(query['alternum'])
            workshop_chosen = Workshop.objects.get(pk=pick)
            ser = WorkshopSerializer(instance=workshop_chosen, data=request.data)
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
            Workshop.objects.get(pk=pick).delete()
            productionlineList = Productionline.objects.filter(workshop_id=pick)
            for productionline in productionlineList:
                productionline.workshop_id = 0
                productionline.save()
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
