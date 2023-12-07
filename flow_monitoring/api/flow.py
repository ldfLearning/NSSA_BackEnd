from response import CustomResponse, ERROR_CODES
from http import HTTPStatus
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.views import APIView
from django.conf import settings
import psutil
from collections import deque

# 初始化历史的网络流量信息，使用队列存储最新的15条，在api维护流量值
history_network_traffic = deque(maxlen=15)

class FlowAPIView(APIView):
    def get_range_record(self,history_network_traffic,start_timestamp,end_timestamp):
        selected_records = [record for record in history_network_traffic if start_timestamp <= record[0] <= end_timestamp]          
        return selected_records
    
    def get(self, request):
        try:
            #防止前端传过来的时间戳包含小数
            start_timestamp = int(float(request.GET.get('start_timestamp'))) #开始时间戳，考虑代码执行时间，时间戳精确到秒级int
            end_timestamp = int(float(request.GET.get('end_timestamp')))   #结束时间戳
            step = int(request.GET.get('step'))

             # 获取当前的网络流量信息
            current_network_traffic = psutil.net_io_counters(pernic=True)
            # 从配置文件中读取默认网卡名称
            default_network_interface = settings.DEFAULT_NETWORK_INTERFACE
            # 计算当前流量包数
            packets = current_network_traffic[default_network_interface].packets_sent + current_network_traffic[default_network_interface].packets_recv
            # 记录当前时间戳
            record_time = int(datetime.now().timestamp())

            # print(record_time)

            # 将当前包数量和记录时间存储
            history_network_traffic.append((record_time, packets))

            # print(history_network_traffic)

            # 计算在时间范围内的包数量
            records = self.get_range_record(history_network_traffic,start_timestamp,end_timestamp)
            packets_in_ranges = []
            step_timestamp = start_timestamp + step

            while step_timestamp <= end_timestamp :
                  tmp_records = self.get_range_record(records,start_timestamp,step_timestamp)
                #   print(tmp_records)
                  if tmp_records:
                     packets_in_range = tmp_records[-1][1] - tmp_records[0][1]
                  else:
                     packets_in_range = 0 
                  packets_in_ranges.append({'timestamp':step_timestamp,'packets':packets_in_range})
                  start_timestamp = step_timestamp
                  step_timestamp = start_timestamp + step
          
            return CustomResponse(data={
                'count':len(packets_in_ranges),
                'total_packets':packets_in_ranges
            })
        except Exception as e:
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )