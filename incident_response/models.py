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
    ip = models.CharField(max_length=20)    # IP地址
    type = models.IntegerField(default=0)   # 攻击类型
    finished = models.BooleanField()        # 是否已处理
    detail = models.TextField()            # 详细信息
    time = models.DateTimeField(auto_now_add=True)  # 发现时间

    class Meta:
        db_table = 'incident_response_event'

# 邮件设置表
class EmailSettings(models.Model):
    id = models.AutoField(primary_key=True)     # 自增主键
    email_recipient = models.CharField(max_length=30)  #收件人邮箱
    email_subject = models.CharField(max_length=100,default='态势告警')    #邮件主题
    email_addresser_name = models.CharField(max_length=100,default='态势感知管理员') #发件人显示名称

    class Meta:
       db_table = 'email_settings'
