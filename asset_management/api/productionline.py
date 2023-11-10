# from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from asset_management.models import Productionline
from asset_management.serializers import ProductionlineSerializer
from rest_framework.response import Response


class ProductionlineBasicView(APIView):
    def get(self, request):
        res = Productionline.objects.all()
        ser = ProductionlineSerializer(instance=res, many=True)
        return Response(ser.data)

    def post(self, request):
        productionline_toadd = ProductionlineSerializer(data=request.data)
        if not productionline_toadd.is_valid():
            return Response(productionline_toadd.errors)
        productionline_toadd.save()
        return Response(productionline_toadd.data)

    def put(self, request, pk):
        workshop_chosen = Productionline.objects.get(pk=pk)
        ser = ProductionlineSerializer(instance=workshop_chosen, data=request.data)
        if not ser.is_valid():
            return Response(ser.errors)
        ser.save()
        return Response(ser.data)

    def delete(self, request, pk):
        Productionline.objects.get(pk=pk).delete()
        return Response({'detail': 'Deleted successfully!'})
