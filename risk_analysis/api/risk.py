from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
#假设其他组的模型表已经建好
from asset_management.models import AssetService
from abnormal_attack.models import AbnormalTraffic,AbnormalHost,AbnormalUser

class RiskAnalysisAPIView(APIView):
    #风险值 = R(A, T, V) = R(L(T, V), F(Ia, Va ))
    def post(self, request):  # 处理前端发送过来的post请求
        res = {'code': 0, 'msg': '分析成功', 'data': {}}
        asset_ip = request.data.get('assetIp')  # 获取资产IP
        asset_value = request.data.get('assetValue')  # 获取资产价值

        try:
            #威胁性
            total_threat_value = 0
            T = 0
            flow_count = AbnormalTraffic.objects.count()  # 获取AbnormalFlow的所有记录数量
            ip_flows = AbnormalTraffic.objects.filter(src_ip=asset_ip)
            ip_flows_count = ip_flows.count()

            #威胁出现频率(T)
            if flow_count != 0:
                 T = ip_flows_count / flow_count
            
            #根据异常流量类型计算威胁值
            for flow in ip_flows:
                threat_value = flow.flow_type+1
                total_threat_value += threat_value

            #脆弱性
            vulnerability_value = 0 
            #脆弱性分数是根据异常用户、异常主机和资产端口开放情况来评估
            services = AssetService.objects.filter(ip=asset_ip)  # 根据资产ID获取资产服务信息
            ports = [service.port for service in services]  # 获取所有端口

            # 危险端口列表
            dangerous_ports = [20, 21, 22, 23, 25, 53, 110, 143, 3306, 3389, 5432]
            # 计算脆弱值
            vulnerable_ports = [port for port in ports if port in dangerous_ports]
            vulnerability_value += len(vulnerable_ports)*2
            
            user_count = AbnormalUser.objects.filter(src_ip=asset_ip).count()  # 查询异常用户
            vulnerability_value += user_count*3

            host_count = AbnormalHost.objects.filter(ip=asset_ip).count()  # 查询异常主机
            vulnerability_value += host_count*5

            #脆弱性(V) 
            V = 1-1/(vulnerability_value+1)

            #风险
            L = T * V
            F = asset_value * V
            R = L * F * total_threat_value

            res['data'] = {
                'total_threat_value': total_threat_value,
                'Va': vulnerability_value,
                'R':round(R)
            }

        except Exception as e:
            print(e)
            res['code'] = -1
            res['msg'] = '分析失败'
            return JsonResponse(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse(res)