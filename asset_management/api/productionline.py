# from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from asset_management.models import *
from asset_management.serializers import ProductionlineSerializer
from rest_framework.response import Response


class ProductionlineBasicView(APIView):
    def get(self, request):
        query = request.query_params.dict()
        page = int(query['page'])
        pageSize = int(query['pageSize'])
        content = str(query['content'])
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
        res = {'total': total, 'totalPage': totalPage, 'nowPage': page, 'data': ser.data}
        return Response(res)

    def post(self, request):
        productionline_toadd = ProductionlineSerializer(data=request.data)
        if not productionline_toadd.is_valid():
            return Response(productionline_toadd.errors)
        productionline_toadd.save()
        return Response(productionline_toadd.data)

    def put(self, request):
        query = request.query_params.dict()
        pick = int(query['alternum'])
        productionline_chosen = Productionline.objects.get(pk=pick)
        ser = ProductionlineSerializer(instance=productionline_chosen, data=request.data)
        if not ser.is_valid():
            return Response(ser.errors)
        ser.save()
        return Response(ser.data)

    def delete(self, request):
        query = request.query_params.dict()
        pick = int(query['deletenum'])
        Productionline.objects.get(pk=pick).delete()
        assetList = Asset.objects.filter(productionline_id=pick)
        for asset in assetList:
            asset.productionline_id = 0
            asset.save()
        return Response({'detail': 'Deleted successfully!'})