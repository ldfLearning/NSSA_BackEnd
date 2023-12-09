import json
import string
from datetime import datetime
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from asset_management.models import *

from apscheduler.schedulers.background import BackgroundScheduler  # 使用它可以使你的定时任务在后台运行
from django_apscheduler.jobstores import DjangoJobStore


# 定时任务，每隔30秒，结合AssetDeviceInfo和远程DeskDevice的内容，对Asset进行更新
def desk_device_update_scheduler():
    try:
        update_scheduler = BackgroundScheduler()
        update_scheduler.add_jobstore(DjangoJobStore(), "default")
        update_scheduler.start()  # 控制定时任务是否开启
        job_id = "desk_device_update_scheduler"
        if update_scheduler.get_job(job_id=job_id):
            update_scheduler.remove_job(job_id=job_id)
        update_scheduler.add_job(desk_device_update, "interval", seconds=30, id=job_id,
                                   name="desk_device_update_scheduler")

    except Exception as e:
        print(e)
        update_scheduler.shutdown()

# 定时任务调用的方法
# 参考DeskDeviceAPI.py中的内容
def desk_device_update():
    # print("desk_device_update start")
    assetdeviceinfos = AssetDeviceInfo.objects.all()
    for assetdeviceinfo in assetdeviceinfos:
        asset_list = Asset.objects.filter(ip=assetdeviceinfo.ip)
        if len(asset_list) != 0:
            asset = asset_list[0]
            asset.device_sn = assetdeviceinfo.device_sn
            asset.save()
            deskdevice_list = DeskDevice.objects.filter(sn=asset.device_sn)
            if len(deskdevice_list) != 0:
                deskdevice = deskdevice_list[0]
                asset.device_type = deskdevice.device_type
                asset.save()
    # print("desk_device_update end")
