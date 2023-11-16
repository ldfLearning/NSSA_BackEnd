from rest_framework.views import APIView
from asset_management.models import Asset
from asset_management.scan.nmap_alive import scanNetwork
from asset_management.serializers import AssetSerializer
from rest_framework.response import Response


class HostScan(APIView):

    def get(self, request):
        res = Asset.objects.all()
        ser = AssetSerializer(instance=res, many=True)
        return Response(ser.data)

    def post(self, request):
        host_toscan = request.data['host']
        print(host_toscan)
        host_got = scanNetwork(host_toscan)
        print(host_got)
        for i in host_got:
            single_host = {}
            single_host["ip"] = i
            host_toadd = AssetSerializer(data=single_host)
            if not host_toadd.is_valid():
                return Response(host_toadd.errors)
            host_toadd.save()
        return Response(host_got)