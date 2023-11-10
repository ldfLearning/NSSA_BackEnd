# from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from asset_management.models import AssetService
from asset_management.serializers import AssetServiceSerializer
from rest_framework.response import Response


class AssetServiceBasicView(APIView):
    def get(self, request):
        res = AssetService.objects.all()
        ser = AssetServiceSerializer(instance=res, many=True)
        return Response(ser.data)

    def post(self, request):
        assetservice_toadd = AssetServiceSerializer(data=request.data)
        if not assetservice_toadd.is_valid():
            return Response(assetservice_toadd.errors)
        assetservice_toadd.save()
        return Response(assetservice_toadd.data)

    def put(self, request, pk):
        workshop_chosen = AssetService.objects.get(pk=pk)
        ser = AssetServiceSerializer(instance=workshop_chosen, data=request.data)
        if not ser.is_valid():
            return Response(ser.errors)
        ser.save()
        return Response(ser.data)

    def delete(self, request, pk):
        AssetService.objects.get(pk=pk).delete()
        return Response({'detail': 'Deleted successfully!'})
