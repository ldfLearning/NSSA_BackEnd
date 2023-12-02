from django.db import models

# Create your models here.

# 应急响应事件表
class IncidentEvent(models.Model):
    FLOW_TYPE_CHOICES = (
        (0, 'AbnormalAttackTraffic'),
        (1, 'AbnormalAttackUser'),
        (2, 'AbnormalAttackHost'),
    )

    id = models.AutoField(primary_key=True) # 自增主键
    type = models.IntegerField(default=0)   # 攻击类型
    finished = models.BooleanField()        # 是否已处理
    content = models.TextField()            # 详细信息
    time = models.DateTimeField(auto_now_add=True)  # 发现时间

    class Meta:
        db_table = 'incident_response_event'
