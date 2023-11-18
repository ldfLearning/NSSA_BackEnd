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
        content = str(query['content'])
        resall = AssetService.objects.all()
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
        res = reschosen[(page - 1) * pageSize: page * pageSize]
        print(res)
        ser = AssetServiceSerializer(instance=res, many=True)
        return Response(ser.data)

    def post(self, request):
        assetservice_toadd = AssetServiceSerializer(data=request.data)
        if not assetservice_toadd.is_valid():
            return Response(assetservice_toadd.errors)
        assetservice_toadd.save()
        return Response(assetservice_toadd.data)

    def put(self, request, pk):
        assetservice_chosen = AssetService.objects.get(pk=pk)
        ser = AssetServiceSerializer(instance=assetservice_chosen, data=request.data)
        if not ser.is_valid():
            return Response(ser.errors)
        ser.save()
        return Response(ser.data)

    def delete(self, request, pk):
        AssetService.objects.get(pk=pk).delete()
        return Response({'detail': 'Deleted successfully!'})
