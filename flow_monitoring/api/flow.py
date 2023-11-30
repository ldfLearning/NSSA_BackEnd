from response import CustomResponse, ERROR_CODES
from http import HTTPStatus
from datetime import datetime,timedelta
from rest_framework.views import APIView
from flow_monitoring.models import NetworkTraffic

class FlowAPIView(APIView):
    def get(self, request):
        try:
            query_count = int(request.GET.get('count', 1))

            # 从数据库中获取最新的count条数据
            latest_data = NetworkTraffic.objects.order_by('-timestamp')[:query_count + 1]

            database_count = len(latest_data)

            total_traffic_data = []
            # 计算流量差值
            for i in range(0,database_count-1, 1):  
                traffic_data = latest_data[i].total_packets - latest_data[i + 1].total_packets
                total_traffic_data.append({'time': latest_data[i].timestamp, 'traffic': traffic_data})

            history_time = latest_data[database_count-1].timestamp

            # 填充total_traffic_data到query_count条
            while len(total_traffic_data) < query_count:
                  total_traffic_data.append({'time': history_time, 'traffic': 0})
                  history_time = history_time - timedelta(minutes=2)

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