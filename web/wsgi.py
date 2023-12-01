"""
WSGI config for web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""


import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

application = get_wsgi_application()

# 在此处定义需要启动时运行的方法

import pickle
import json

from kafka import KafkaConsumer
from abnormal_attack.models import AbnormalTraffic, AbnormalHost, AbnormalUser
from incident_response.models import IncidentEvent

MSG_TYPE_TRAFFIC = 0
MSG_TYPE_HOST = 1
MSG_TYPE_USER = 2


def dealMessageEvents(topic, group_id, bootstrap_servers):
    print("son thread")
    # 消息队列接收配置
    msg_consumer = KafkaConsumer(
        topic,
        group_id=group_id,
        bootstrap_servers=bootstrap_servers
    )
    # 开始消费
    for m in msg_consumer:
        msg = pickle.loads(m.value)
        data = msg.data
        # 异常流量
        if msg.type == MSG_TYPE_TRAFFIC:
            # 保存异常流量信息
            traffic = AbnormalTraffic(
                type=data.type, time=data.time, src_ip=data.src_ip, dst_ip=data.dst_ip, detail=data.detail)
            traffic.save()
            # 记录日志
            traffic_log = IncidentEvent(
                type='AbnormalAttackTraffic', time=data.time, finished=False, content=json.dumps(data)
            )
            traffic_log.save()

        # 异常主机
        elif msg.type == MSG_TYPE_HOST:
            # 保存异常主机信息
            traffic = AbnormalHost(
                ip=data.ip, name=data.name, errprint=data.errprint, time=data.time)
            traffic.save()
            # 记录日志
            host_log = IncidentEvent(
                type='AbnormalAttackHost', time=data.time, finished=False, content=json.dumps(data)
            )
            host_log.save()

        # 异常用户
        elif msg.type == MSG_TYPE_USER:
            # 保存异常用户信息
            traffic = AbnormalUser(
                type=data.type, time=data.time, user_name=data.user_name, topic=data.topic, src_ip=data.src_ip)
            traffic.save()
            # 记录日志
            user_log = IncidentEvent(
                type='AbnormalAttackUser', time=data.time, finished=False, content=json.dumps(data)
            )
            user_log.save()

# 多线程任务
import threading
threading.Thread(
    target=dealMessageEvents,
    args=('abnormal-events', 'backend', 'localhost:9092'),
    daemon=True
).start()