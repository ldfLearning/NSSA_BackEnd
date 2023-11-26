from django.db import models

# Create your models here.

# 异常攻击发现表
class AbnormalTraffic(models.Model):
    id = models.AutoField(primary_key=True)     # 自增主键
    type = models.IntegerField(default=0)       # 攻击类型
    time = models.DateTimeField()               # 发现时间
    src_ip = models.CharField(max_length=20)    # 源IP
    dst_ip = models.CharField(max_length=20)    # 目的IP
    detail = models.CharField(max_length=200)   # 详细信息

# 异常主机发现表
class AbnormalHost(models.Model):
    id = models.AutoField(primary_key=True)             # 自增主键
    ip = models.CharField(max_length=20)                # 资产IP
    name = models.CharField(max_length=100, default='') # 资产名称
    errprint = models.CharField(max_length=200, default='')  # 异常信息
    time = models.DateTimeField()                 # 发现时间

# 用户行为检测表
class AbnormalUser(models.Model):
    id = models.AutoField(primary_key=True)     # 自增主键
    type = models.IntegerField(default=0)       # 攻击类型
    time = models.DateTimeField()               # 发现时间
    user_name = models.CharField(max_length=50) # 用户姓名
    topic = models.CharField(max_length=200)    # 主题名称
    src_ip = models.CharField(max_length=20)    # IP