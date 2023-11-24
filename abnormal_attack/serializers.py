from rest_framework import serializers
from .models import AbnormalTraffic

class AbnormalTrafficSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbnormalTraffic
        fields = '__all__'