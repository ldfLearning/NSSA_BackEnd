from datetime import datetime
import psutil
from django.conf import settings
from flow_monitoring.models import NetworkTraffic

def set_traffic_value():
    try:
        # 获取当前的网络流量信息
        current_network_traffic = psutil.net_io_counters(pernic=True)
        # 从配置文件中读取默认网卡名称
        default_network_interface = settings.DEFAULT_NETWORK_INTERFACE

        # 计算总数
        total_packets = current_network_traffic[default_network_interface].packets_sent + current_network_traffic[default_network_interface].packets_recv

         # 检查表中的数据数量
        data_count = NetworkTraffic.objects.count()

        # 如果数据数量超过11条，则删除最旧的数据
        if data_count >= 11:
            oldest_record = NetworkTraffic.objects.order_by('timestamp').first()
            oldest_record.delete()
       
        # 创建数据库记录
        NetworkTraffic.objects.create(
            interface_name=default_network_interface,
            total_packets=total_packets
        )
        
        print(f"Traffic data saved at {datetime.now()} for {default_network_interface}")
    except Exception as e:
        print(f"Error saving traffic data: {e}")

