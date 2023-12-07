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
    update_time = models.CharField(max_length=50, default='', null=True, blank=True)  # 更新时间