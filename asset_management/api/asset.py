# from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from asset_management.models import Asset
from asset_management.serializers import AssetSerializer
from rest_framework.response import Response


class AssetBasicView(APIView):
    def get(self, request):
        res = Asset.objects.all()
        ser = AssetSerializer(instance=res, many=True)
        return Response(ser.data)

    def post(self, request):
        asset_toadd = AssetSerializer(data=request.data)
        if not asset_toadd.is_valid():
            return Response(asset_toadd.errors)
        asset_toadd.save()
        return Response(asset_toadd.data)


class AssetToolView(APIView):
    def get(self, request, pk):
        workshop_chosen = Asset.objects.get(pk=pk)
        ser = AssetSerializer(instance=workshop_chosen)
        return Response(ser.data)

    def put(self, request, pk):
        workshop_chosen = Asset.objects.get(pk=pk)
        ser = AssetSerializer(instance=workshop_chosen, data=request.data)
        if not ser.is_valid():
            return Response(ser.errors)
        ser.save()
        return Response(ser.data)

    def delete(self, request, pk):
        Asset.objects.get(pk=pk).delete()
        return Response({'detail': '删除成功！！'})
