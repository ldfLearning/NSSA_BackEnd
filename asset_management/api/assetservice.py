# from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from asset_management.models import AssetService
from asset_management.serializers import AssetServiceSerializer
from rest_framework.response import Response


class AssetServiceBasicView(APIView):
    def get(self, request):
        query = request.query_params.dict()
        page = int(query['page'])
        pageSize = int(query['pageSize'])
        assetid = int(query['assetid'])
        content = str(query['content'])
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
        res = {'total': total, 'totalPage': totalPage, 'nowPage': page, 'data': ser.data}
        return Response(res)

    def post(self, request):
        assetservice_toadd = AssetServiceSerializer(data=request.data)
        if not assetservice_toadd.is_valid():
            return Response(assetservice_toadd.errors)
        assetservice_toadd.save()
        return Response(assetservice_toadd.data)

    def put(self, request):
        query = request.query_params.dict()
        pick = int(query['alternum'])
        assetservice_chosen = AssetService.objects.get(pk=pick)
        ser = AssetServiceSerializer(instance=assetservice_chosen, data=request.data)
        if not ser.is_valid():
            return Response(ser.errors)
        ser.save()
        return Response(ser.data)

    def delete(self, request):
        query = request.query_params.dict()
        pick = int(query['deletenum'])
        AssetService.objects.get(pk=pick).delete()
        return Response({'detail': 'Deleted successfully!'})
