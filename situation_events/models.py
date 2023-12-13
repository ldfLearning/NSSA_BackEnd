from django.db import models

# Create your models here.

class SituationEvent(models.Model):
    id = models.AutoField(primary_key=True)  #自增主键id
    event_type = models.IntegerField() # 事件类型：DDoS, Webshell...
    happened_at = models.DateTimeField() # 态势事件检测时间
    event_info = models.TextField() # 事件信息

    class Meta:
        db_table = 'situation_events'
