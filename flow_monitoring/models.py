from django.db import models

class NetworkTraffic(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    interface_name = models.CharField(max_length=50)
    total_packets = models.BigIntegerField()