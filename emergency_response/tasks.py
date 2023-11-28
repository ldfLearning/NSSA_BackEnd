from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone
from email.utils import formataddr
from django.core.mail import send_mail
from abnormal_attack.models import AbnormalTraffic,AbnormalHost,AbnormalUser
from .models import AbnormalWarning
from django.core.exceptions import ValidationError

def check_and_send():
    # warning_results = monitor_warning()
    # print('time')
    # if len(warning_results) > 0:
    #    print('监测到异常攻击，开始发送邮件并插入数据库')
    #    insert_warning_data(warning_results)
    #    send_email_view(warning_results)
    send_email_view()

def insert_warning_data(warning_results):
    for warning_result in warning_results:
        # 检查告警类型是否符合枚举类型
        try:
            type_choice = AbnormalWarning.ABNORMAL_TYPE_CHOICES[warning_result['type']]
        except IndexError:
            # 如果告警类型不符合枚举类型，则跳过该告警结果
            continue

        # 创建新的告警记录
        try:
            AbnormalWarning.objects.create(
                type=warning_result['type'],
                time=warning_result['time'],
                ip=warning_result['ip'],
                detail=warning_result['detail'],
                status=warning_result['status']
            )
        except ValidationError:
            # 如果数据验证失败，则跳过该告警结果
            continue

def monitor_warning():
    # 计算当前时间和2分钟前的时间
    end_time = timezone.now()
    print(end_time)
    start_time = end_time - timedelta(minutes=2)
    print(start_time)
    # 查询最近2分钟内的新入库数据
    recent_traffic_entries = AbnormalTraffic.objects.filter(time__range=(start_time, end_time))
    recent_user_entries = AbnormalUser.objects.filter(time__range=(start_time, end_time),type=1)
    recent_host_entries = AbnormalHost.objects.filter(time__range=(start_time, end_time))
    
    warning_results = []
    warning_result = {}
    # 获取查询结果中的字段值
    for entry in recent_traffic_entries:
        warning_result['ip'] = entry.dst_ip
        warning_result['type'] = 0
        warning_result['time'] = entry.time
        warning_result['detail'] = '来自'+entry.src_ip+'的异常流量攻击：'+entry.detail
        warning_result['status'] = False
        warning_results.append(warning_result)

    for entry in recent_user_entries:
        warning_result['ip'] = entry.src_ip
        warning_result['type'] = 1
        warning_result['time'] = entry.time
        warning_result['detail'] = '存在异常用户'+entry.user_name+'：'+entry.topic
        warning_result['status'] = False
        warning_results.append(warning_result)

    for entry in recent_host_entries:
        warning_result['ip'] = entry.ip
        warning_result['type'] = 2
        warning_result['time'] = entry.time
        warning_result['detail'] = '异常主机行为：'+entry.detail
        warning_result['status'] = False
        warning_results.append(warning_result)

    return warning_results


def send_email_view():
    print('email:'+settings.EMAIL_RECIPIENT)
    subject = settings.EMAIL_SUBJECT_PREFIX+' 态势告警'
    message = 'warning:'
    from_name = settings.EMAIL_ADDRESSER_SHOW  # 发件人显示
    from_email = settings.EMAIL_HOST_USER  # 发件人邮箱
    recipient_list = [settings.EMAIL_RECIPIENT]  # 收件人邮箱列表

    # 使用formataddr函数设置发件人名称和邮箱地址
    from_address = formataddr((from_name, from_email))

    send_mail(subject, message, from_address, recipient_list)

    print("fas")