from http import HTTPStatus
from django.conf import settings
import psutil
from collections import deque
from rest_framework.views import APIView
from response import CustomResponse, ERROR_CODES

class FlowAPIView(APIView):
    # 初始化历史的网络流量信息，使用队列存储
    history_network_traffic = deque([psutil.net_io_counters(pernic=True)] * 11, maxlen=11)

    def get(self, request):
        try:
            # 获取前端传递的时间段数量，默认为1,不超过10
            count = int(request.GET.get('count', 1))
            # 获取当前的网络流量信息
            current_network_traffic = psutil.net_io_counters(pernic=True)
            # 入队最新的网络流量信息
            self.history_network_traffic.appendleft(current_network_traffic)

            # 从配置文件中读取默认网卡名称
            default_network_interface = settings.DEFAULT_NETWORK_INTERFACE

            total_traffic_data = []
            # 计算流量差异
            for i in range(count):
                bytes_sent = self.history_network_traffic[i][default_network_interface].bytes_sent - self.history_network_traffic[i + 1][default_network_interface].bytes_sent
                bytes_recv = self.history_network_traffic[i][default_network_interface].bytes_recv - self.history_network_traffic[i + 1][default_network_interface].bytes_recv

                # 计算总流量
                total_traffic = bytes_sent + bytes_recv

                total_traffic_data.append(total_traffic)

            response_data = {
                'total_traffic': total_traffic_data,
            }
            
            return CustomResponse(data=response_data)

        except Exception as e:
              return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )