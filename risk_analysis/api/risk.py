from http import HTTPStatus
from rest_framework.views import APIView
from response import CustomResponse, ERROR_CODES,ERROR_MESSAGES
from risk_analysis.models import AssetRisk
from risk_analysis.serializers import AssetRiskSerializer
#假设其他组的模型表已经建好
from asset_management.models import AssetService 
from abnormal_attack.models import AbnormalTraffic,AbnormalHost,AbnormalUser

class RiskAPIView(APIView):
     #从表查询
    def get(self,request):
        try:
            asset_id = request.GET.get('asset_id')  # 获取资产id
            asset_risk = AssetRisk.objects.get(asset_id=asset_id)
            serializer = AssetRiskSerializer(asset_risk)
            return CustomResponse(data=serializer.data)
        except AssetRisk.DoesNotExist:
            return CustomResponse(
                code=ERROR_CODES['NOT_FOUND'],
                msg=ERROR_MESSAGES['NOT_FOUND'],
                data={},
                status=HTTPStatus.NOT_FOUND
            )
        
    #新增资产id，为了get请求和重新计算的api测试用，后面不需要这个api，删除即可
    def post(self,request):
        try:
            asset_id = request.data.get('asset_id')  # 获取资产id
            # 创建并保存 AssetRisk 对象，其他字段默认为0
            AssetRisk.objects.create(asset_id=asset_id)
            return CustomResponse()
        except AssetRisk.DoesNotExist:
            return CustomResponse(
                code=ERROR_CODES['NOT_FOUND'],
                msg=ERROR_MESSAGES['NOT_FOUND'],
                data={},
                status=HTTPStatus.NOT_FOUND
            )

class RiskCalculationAPIView(APIView):
    DANGEROUS_PORTS = [20, 21, 22, 23, 25, 53, 110, 143, 3306, 3389, 5432]
    PORT_VULNERABILITY_WEIGHT = 2
    USER_VULNERABILITY_WEIGHT = 3
    HOST_VULNERABILITY_WEIGHT = 5

    def calculate_vulnerability_value(self, asset_ip):
        services = AssetService.objects.filter(ip=asset_ip)
        ports = [service.port for service in services]

        vulnerable_ports = [port for port in ports if port in self.DANGEROUS_PORTS]
        port_vulnerability = len(vulnerable_ports) * self.PORT_VULNERABILITY_WEIGHT

        user_count = AbnormalUser.objects.filter(src_ip=asset_ip, type=1).count()
        user_vulnerability = user_count * self.USER_VULNERABILITY_WEIGHT

        host_count = AbnormalHost.objects.filter(ip=asset_ip).count()
        host_vulnerability = host_count * self.HOST_VULNERABILITY_WEIGHT

        total_vulnerability = port_vulnerability + user_vulnerability + host_vulnerability
        return total_vulnerability

    #计算风险值
    def post(self, request):
        try:
            asset_id = request.data.get('asset_id') # 获取资产id
            asset_value = request.data.get('asset_value') # 获取资产价值
            asset_ip = AssetService.objects.get(asset_id=asset_id).ip #从资产id里面获取资产ip，一个资产id只有一个资产ip

            #威胁性
            total_threat_value = 0
            flow_count = AbnormalTraffic.objects.count()
            ip_flows = AbnormalTraffic.objects.filter(src_ip=asset_ip)
            ip_flows_count = ip_flows.count()

            #威胁出现频率(T)
            T = ip_flows_count / flow_count if flow_count != 0 else 0

            #根据异常流量类型计算威胁值
            for flow in ip_flows:
                threat_value = flow.type+1
                total_threat_value += threat_value

            #脆弱性
            vulnerability_value = self.calculate_vulnerability_value(asset_ip)

            V = 1 - 1 / (vulnerability_value + 1)

            L = T + V
            F = asset_value * L
            R = F * total_threat_value

            data = {
                'total_threat_value': total_threat_value,
                'Va': vulnerability_value,
                'R': round(R)
            }

            #更新表数据
            AssetRisk.objects.filter(asset_id=asset_id).update(
                asset_value=asset_value,
                threat_value=total_threat_value,
                vulnerability_value=vulnerability_value,
                risk_value=round(R)
            )

            return CustomResponse(data=data)

        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        