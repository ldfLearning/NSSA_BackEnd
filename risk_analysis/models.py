from django.db import models

# Create your models here.
class AssetRisk(models.Model):
    id = models.AutoField(primary_key=True)     # 自增主键
    asset_id = models.IntegerField()  # 资产id
    asset_value = models.IntegerField(default=0) #资产价值
    threat_value = models.IntegerField(default=0) #威胁值
    vulnerability_value = models.IntegerField(default=0) #脆弱值
    risk_value = models.IntegerField(default=0) #风险值

    class Meta:
       db_table = 'asset_risk'