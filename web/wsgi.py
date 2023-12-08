"""
WSGI config for web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""


import os

from django.core.wsgi import get_wsgi_application
from asset_management.api.DeskDeviceAutoAPI import desk_device_update_scheduler


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

application = get_wsgi_application()

# 在此处定义需要启动时运行的方法

import pickle
import json

from kafka import KafkaConsumer
from abnormal_attack.models import AbnormalTraffic, AbnormalHost, AbnormalUser
from incident_response.models import IncidentEvent
from incident_response.models import EmailSettings
from django.conf import settings
from django.core.mail import send_mail
from email.utils import formataddr

MSG_TYPE_TRAFFIC = 0
MSG_TYPE_HOST = 1
MSG_TYPE_USER = 2

def getEmailSettings():
    try:
        # 获取唯一的 EmailSettings 记录
        email_settings = EmailSettings.objects.get()
        return email_settings
    except Exception as e:
        print(e)

#发送邮件
def send_email_view(warning_msg):
    try:
        emailsetting = getEmailSettings()
        subject = emailsetting.email_subject #主题
        from_name = emailsetting.email_addresser_name  # 发件人显示
        from_email = settings.EMAIL_HOST_USER  # 发件人邮箱
        message = warning_msg
        recipient_list = [emailsetting.email_recipient]  # 收件人邮箱列表
        # 使用formataddr函数设置发件人名称和邮箱地址
        from_address = formataddr((from_name, from_email))
        send_mail(subject, message, from_address, recipient_list)
    except Exception as e:
        print(e)


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
                type='AbnormalAttackTraffic', ip=data.dst_ip, time=data.time, finished=False, detail=json.dumps(data)
            )
            traffic_log.save()
            # 发送邮件
            warning_msg = data.time+',  '+data.dst_ip+'的机器正在遭遇异常流量威胁，详细情况如下：'+data.detail
            send_email_view(warning_msg)

        # 异常主机
        elif msg.type == MSG_TYPE_HOST:
            # 保存异常主机信息
            traffic = AbnormalHost(
                ip=data.ip, name=data.name, detail=data.detail, time=data.time)
            traffic.save()
            # 记录日志
            host_log = IncidentEvent(
                type='AbnormalAttackHost', ip=data.ip, time=data.time, finished=False, detail=json.dumps(data)
            )
            host_log.save()
            # 发送邮件
            warning_msg = data.time+',  '+data.ip+'的机器存在异常主机行为，详细情况如下：'+data.detail
            send_email_view(warning_msg)

        # 异常用户
        elif msg.type == MSG_TYPE_USER:
            # 保存异常用户信息
            traffic = AbnormalUser(
                type=data.type, time=data.time, user_name=data.user_name, topic=data.topic, src_ip=data.src_ip)
            traffic.save()
            # 记录日志
            user_log = IncidentEvent(
                type='AbnormalAttackUser', ip=data.src_ip, time=data.time, finished=False, detail=json.dumps(data)
            )
            user_log.save()
             # 发送邮件
            warning_msg = data.time+',  '+data.src_ip+'的机器存在异常用户行为，详细情况如下：'+data.topic
            send_email_view(warning_msg)

# 多线程任务
import threading
threading.Thread(
    target=dealMessageEvents,
    args=('abnormal-events', 'backend', 'localhost:9092'),
    daemon=True
).start()