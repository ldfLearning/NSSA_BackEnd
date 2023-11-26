from django.db import models

# Create your models here.
# 告警信息表
class AbnormalWarning(models.Model):
    ABNORMAL_TYPE_CHOICES = (
        (0, '异常流量'),
        (1, '异常用户'),
        (2, '异常主机'),
        # 添加更多的攻击类型
    )
    id = models.AutoField(primary_key=True)     # 自增主键
    type = models.IntegerField(choices=ABNORMAL_TYPE_CHOICES, default=0)   # 告警类型
    time = models.DateTimeField()               # 发现时间
    ip = models.CharField(max_length=20)        # 源IP
    detail = models.CharField(max_length=200)   # 详细信息
    status = models.BooleanField(default=False)     # 事件状态