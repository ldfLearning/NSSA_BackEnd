from rest_framework.views import APIView
from asset_management.models import Asset
from asset_management.serializers import AssetSerializer
from rest_framework.response import Response


class AssetBasicView(APIView):

    def get(self, request):
        query = request.query_params.dict()
        page = int(query['page'])
        pageSize = int(query['pageSize'])
        content = str(query['content'])
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
        res = {'total': total, 'totalPage': totalPage, 'nowPage': page, 'data': ser.data}
        return Response(res)

    def post(self, request):
        asset_toadd = AssetSerializer(data=request.data)
        if not asset_toadd.is_valid():
            return Response(asset_toadd.errors)
        asset_toadd.save()
        return Response(asset_toadd.data)

    def put(self, request):
        query = request.query_params.dict()
        pick = int(query['alternum'])
        asset_chosen = Asset.objects.get(pk=pick)
        ser = AssetSerializer(instance=asset_chosen, data=request.data)
        if not ser.is_valid():
            return Response(ser.errors)
        ser.save()
        return Response(ser.data)

    def delete(self, request):
        query = request.query_params.dict()
        pick = int(query['deletenum'])
        Asset.objects.get(pk=pick).delete()
        return Response({'detail': 'Deleted successfully!'})
