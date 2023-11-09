import json
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
#假设其他组的模型表已经建好
from asset_management.models import Asset,AssetService
from abnormal_attack.models import AbnormalFlow,AbnormalUser,AbnormalHost

class RiskAnalysisAPIView(APIView):
    #风险值 = R(A, T, V) = R(L(T, V), F(Ia, Va ))
    def post(self, request):  # 处理前端发送过来的post请求
        res = {'code': 0, 'msg': '分析成功', 'data': {}}
        asset_ip = request.data.get('assetIp')  # 获取资产IP
        asset_value = request.data.get('assetValue')  # 获取资产价值

        try:
            #威胁性
            total_threat_value = 0
            threat_values = []  # 存储每个threat_value的列表
            T = 0
            flow_count = AbnormalFlow.objects.count()  # 获取AbnormalFlow的所有记录数量
            ip_flows = AbnormalFlow.objects.filter(src_ip=asset_ip)
            ip_flows_count = ip_flows.count()

            #威胁出现频率(T)
            if flow_count != 0:
                 T = ip_flows_count / flow_count
            
            #根据异常流量类型计算威胁值
            for flow in ip_flows:
                threat_value = flow.flow_type
                total_threat_value += threat_value
                threat_values.append(threat_value)  # 将每个threat_value添加到列表中

            res['data']['threatening'] = {
                'total_threat_value': total_threat_value,
                'T': T,  
                'threat_value': threat_values  
            }

            #脆弱性
            vulnerability_value = 1 #即Va至少为1，确保（1-1/va）在0-1之间
            #脆弱性分数是根据异常用户、异常主机和资产端口开放情况来评估
            asset = Asset.objects.filter(ip=asset_ip).first()  # 根据资产IP获取资产信息
            if asset:
                services = AssetService.objects.filter(asset_id=asset.id)  # 根据资产ID获取资产服务信息
                ports = [service.port for service in services]  # 获取所有端口

                # 危险端口列表
                dangerous_ports = [20, 21, 22, 23, 25, 53, 110, 143, 3306, 3389, 5432]
                # 计算脆弱值
                vulnerable_ports = [port for port in ports if port in dangerous_ports]
                vulnerability_value += len(vulnerable_ports)*2
            
            user_count = AbnormalUser.objects.filter(ip=asset_ip).count()  # 查询异常用户
            vulnerability_value += len(user_count)*3

            host_count = AbnormalHost.objects.filter(ip=asset_ip).count()  # 查询异常主机
            vulnerability_value += len(host_count)*5

            #脆弱性(V) 
            V = 1-1/vulnerability_value

            res['data']['vulnerability'] = {
                'V': V,
                'Va': vulnerability_value,  
            }

            #风险
            L = T * V
            F = asset_value * V
            R = L * F * total_threat_value
            if(L<0.3):
                risk_level = "低危"
            elif(L>=0.3 and L<0.7):
                risk_level = "中危"
            elif(L>=0.7):
                risk_level = "高危"

            res['data']['risk'] = {
                "L":L,
                "F":F,
                "R":R,
                "level":risk_level 
            }

        except Exception as e:
            print(e)
            res['code'] = -1
            res['msg'] = '分析失败'
            return JsonResponse(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse(res)


