"""
WSGI config for web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

from kafka import KafkaConsumer
import pickle
import os

from django.core.wsgi import get_wsgi_application
from abnormal_attack.models import AbnormalTraffic, AbnormalHost, AbnormalUser

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

application = get_wsgi_application()

# 在此处定义需要启动时运行的方法

MSG_TYPE_TRAFFIC = 0
MSG_TYPE_HOST = 1
MSG_TYPE_USER = 2


def dealMessageEvents(topic, group_id, bootstrap_servers):
    # 消息队列接收配置
    msg_consumer = KafkaConsumer(
        topics=topic,
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
            # TODO: 记录日志

        # 异常主机
        elif msg.type == MSG_TYPE_HOST:
            # 保存异常主机信息
            traffic = MSG_TYPE_HOST(
                ip=data.ip, name=data.name, errprint=data.errprint, time=data.time)
            traffic.save()
            # TODO: 记录日志

        # 异常用户
        elif msg.type == MSG_TYPE_USER:
            # 保存异常用户信息
            traffic = AbnormalUser(
                type=data.type, time=data.time, user_name=data.user_name, topic=data.topic, src_ip=data.src_ip)
            traffic.save()
            # TODO: 记录日志
