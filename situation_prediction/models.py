from django.db import models


# Create your models here.

class Situation(models.Model):
    # 存储近5分钟的态势值，每一分钟存储一次
    first_situation_value = models.FloatField(default=1000)
    second_situation_value = models.FloatField(default=1000)
    third_situation_value = models.FloatField(default=1000)
    fourth_situation_value = models.FloatField(default=1000)
    fifth_situation_value = models.FloatField(default=1000)
    prediction_value = models.FloatField(default=1000)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "situation_prediction_value"
        verbose_name = "态势值预测"
        verbose_name_plural = verbose_name
