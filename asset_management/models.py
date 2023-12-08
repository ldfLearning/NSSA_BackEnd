from django.db import models


# Create your models here.

# 某一资产，必然属于某一车间下的某一产线中

# 车间信息表 （1级）
class Workshop(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    name = models.CharField(max_length=100)  # 名称/
    shortened = models.CharField(max_length=50, default='', null=True, blank=True)  # 简称/
    productionline_number = models.IntegerField(default=0)  # 产线数量/


# 产线信息表 （2级）
class Productionline(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    name = models.CharField(max_length=100)  # 名称/
    shortened = models.CharField(max_length=50, default='', null=True, blank=True)  # 简称/
    workshop_id = models.IntegerField(default=0)  # 所属车间id
    asset_number = models.IntegerField(default=0)  # 资产数量/


# 资产信息表 （3级）
class Asset(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    ip = models.CharField(max_length=20, default='')  # 资产IP
    name = models.CharField(max_length=100, default='', null=True, blank=True)  # 资产名称
    position = models.CharField(max_length=100, default='', null=True, blank=True)  # 位置
    device_sn = models.CharField(max_length=100, default='', null=True, blank=True)  # 设备SN
    device_vendor = models.CharField(max_length=100, default='', null=True, blank=True)  # 设备厂商
    device_type = models.CharField(max_length=100, default='', null=True, blank=True)  # 设备类型
    device_working_hours = models.CharField(max_length=100, default='', null=True, blank=True)  # 设备工作时长
    cpu_used = models.FloatField(default=0, null=True, blank=True)  # CPU 使用率
    remain_mem = models.FloatField(default=0, null=True, blank=True)  # 剩余内存
    remain_harddisk = models.FloatField(default=0, null=True, blank=True)  # 剩余硬盘
    network_speed = models.FloatField(default=0, null=True, blank=True)  # 网速
    os = models.CharField(max_length=100, default='', null=True, blank=True)  # 操作系统
    mac = models.CharField(max_length=80, default='', null=True, blank=True)  # MAC地址
    update_time = models.CharField(max_length=50, default='', null=True, blank=True)  # 更新时间
    # workshop_id = models.IntegerField(default=0)  # 所属车间id 冗余
    productionline_id = models.IntegerField(default=0)  # 所属产线id


# 源于NCLINK网关的mosquitto日志
# 资产服务信息表
class AssetService(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    asset_id = models.IntegerField(default=0)  # 资产id
    ip = models.CharField(max_length=20)  # 资产IP
    port = models.IntegerField()  # 端口
    name = models.CharField(max_length=45, default='', null=True, blank=True)  # 服务名称
    state = models.CharField(max_length=10, default='', null=True, blank=True)  # 状态
    product = models.CharField(max_length=45, default='', null=True, blank=True)  # 产品
    version = models.CharField(max_length=45, default='', null=True, blank=True)  # 版本
    cpe = models.CharField(max_length=100, default='', null=True, blank=True)  # 通用平台枚举项
    extrainfo = models.CharField(max_length=60, default='', null=True, blank=True)  # 其他信息
    update_time = models.CharField(max_length=50, default='', null=True, blank=True)  # 更新时间


# Jtopo中新增设备
class JtopoDevices(models.Model):
    name = models.CharField(max_length=100)  # 新增设备名称
    type = models.CharField(max_length=50, default='')  # 新增设备类型
    title = models.CharField(max_length=200, default='', null=True, blank=True)  # 新增设备简单描述
    imgUrl = models.CharField(max_length=100, default='')  # 新增设备图标路径，计划放在asset_management/files/jtopo_img/下


# 拓扑图文件ID和对应的文件路径表
class JtopoFilePath(models.Model):
    topo_id = models.CharField(max_length=100)  # topo图ID
    topo_src = models.CharField(max_length=200)  # topo文件路径


# 资产信息表中的设备SN和设备类型
class AssetDeviceInfo(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    ip = models.CharField(max_length=20)  # 日志中的资产IP
    device_sn = models.CharField(max_length=100, default='')  # 日志中的设备SN
    time = models.CharField(max_length=50, default='', null=True, blank=True)  # 更新时间


# 远端的数据库中的资产相关信息表
# 不可对其做迁移操作
class DeskDevice(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(null=True, blank=True)
    device_flag = models.BooleanField(null=True, blank=True)
    device_status = models.CharField(max_length=100, null=True, blank=True)
    device_type = models.CharField(max_length=100, null=True, blank=True)
    img_path = models.CharField(max_length=500, null=True, blank=True)
    is_register = models.BooleanField(default=False, null=True, blank=True)
    model = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    organize_id = models.IntegerField(default=101, null=True, blank=True, verbose_name='组织id')
    part_cnt = models.CharField(max_length=10, null=True, blank=True)
    probe_version = models.CharField(max_length=100, null=True, blank=True)
    register_time = models.DateTimeField(null=True, blank=True)
    sn = models.CharField(max_length=100, null=True, blank=True, unique=True)
    status = models.CharField(max_length=5, null=True, blank=True, default='0')
    update_time = models.DateTimeField(null=True, blank=True)
    warning_info = models.BooleanField(null=True, blank=True)

    class Meta:
        managed = False  # 设置为False表示Django不管理该表
        app_label = "iNCManager"
        db_table = 'desk_device'  # 表名
        indexes = [
            models.Index(fields=['sn'], name='UKih4igmf3itu7wbglmi0pbq46w'),
        ]
from django.db import models

# Create your models here.
# 目前安全风险分析测试用，等资产管理组合并的时候删除即可
# 资产服务信息表
class AssetService(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    asset_id = models.IntegerField(default=0)  # 资产id
    ip = models.CharField(max_length=20)  # 资产IP
    port = models.IntegerField()  # 端口
    name = models.CharField(max_length=45, default='', null=True, blank=True)  # 服务名称
    state = models.CharField(max_length=10, default='', null=True, blank=True)  # 状态
    product = models.CharField(max_length=45, default='', null=True, blank=True)  # 产品
    version = models.CharField(max_length=45, default='', null=True, blank=True)  # 版本
    cpe = models.CharField(max_length=100, default='', null=True, blank=True)  # 通用平台枚举项
    extrainfo = models.CharField(max_length=60, default='', null=True, blank=True)  # 其他信息
    update_time = models.Cha