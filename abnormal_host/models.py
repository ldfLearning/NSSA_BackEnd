from django.db import models


# Create your models here.
class ErrInfo(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    ip = models.CharField(max_length=20)  # 资产IP
    name = models.CharField(max_length=100, default='')  # 资产名称
    errprint = models.CharField(max_length=200, default='')  # 异常信息
    time = models.CharField(max_length=50, default='')  # 异常时间

    class Meta:
        db_table = 'err info'