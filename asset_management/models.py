from django.db import models

# Create your models here.

# 某一资产，必然属于某一车间下的某一产线中

# 车间信息表 （1级）
class Workshop(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    name = models.CharField(max_length=100)  # 名称/
    shortened = models.CharField(max_length=50, default='')  # 简称/
    productionline_number = models.IntegerField(default=0)  # 产线数量/

# 产线信息表 （2级）
class Productionline(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    name = models.CharField(max_length=100)  # 名称/
    workshop_id = models.IntegerField(default=0)  # 车间id
    shortened = models.CharField(max_length=50, default='')  # 简称/
    asset_number = models.IntegerField(default=0)  # 资产数量/

# 资产信息表 （3级）
class Asset(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    ip = models.CharField(max_length=20)  # 资产IP
    asset_name = models.CharField(max_length=100, default='')  # 资产名称
    position = models.CharField(max_length=100, default='')  # 位置
    device_sn = models.CharField(max_length=100, default='')  # 设备SN
    device_vendor = models.CharField(max_length=100, default='')  # 设备厂商
    device_type = models.CharField(max_length=100, default='')  # 设备类型
    device_working_hours = models.CharField(max_length=100, default='')  # 设备工作时长
    cpu_used = models.FloatField(default=0)  # CPU 使用率
    remain_mem = models.FloatField(default=0)  # 剩余内存
    remain_harddisk = models.FloatField(default=0)  # 剩余硬盘
    network_speed = models.FloatField(default=0)  # 网速
    os = models.CharField(max_length=100, default='')  # 操作系统
    mac = models.CharField(max_length=80, default='')  # MAC地址
    update_time = models.CharField(max_length=50, default='')  # 更新时间
    # workshop_id = models.IntegerField(default=0)  # 所属车间id 冗余
    productionline_id = models.IntegerField(default=0)  # 所属产线id

# 资产IP和资产名称对应信息表 待定
# 源于NCLINK网关的mosquitto日志

# 资产服务信息表
class AssetService(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    asset_id = models.IntegerField(default=0)  # 资产id
    port = models.IntegerField()  # 端口
    state = models.CharField(max_length=10, default='')  # 状态
    name = models.CharField(max_length=45, default='')  # 服务名称
    product = models.CharField(max_length=45, default='')  # 产品
    version = models.CharField(max_length=45, default='')  # 版本
    cpe = models.CharField(max_length=100, default='')  # 通用平台枚举项
    extrainfo = models.CharField(max_length=60, default='')  # 其他信息
    update_time = models.CharField(max_length=50, default='')  # 更新时间

# Jtopo中新增设备
class JtopoDevices(models.Model):
    name = models.CharField(max_length=100)  # 新增设备名称
    type = models.CharField(max_length=50, default='')  # 新增设备类型
    title = models.CharField(max_length=200, default='')  # 新增设备简单描述
    imgUrl = models.CharField(max_length=100, default='')  # 新增设备图标路径，计划放在JtopoImg文件夹下

# 拓扑图文件ID和对应的文件路径表
class JtopoFilePath(models.Model):
    topo_id = models.CharField(max_length=100)  # topo图ID
    topo_src = models.CharField(max_length=200)  # topo文件路径
