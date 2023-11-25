from rest_framework import serializers
from .models import AbnormalTraffic

class AbnormalTrafficSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbnormalTraffic
        fields = '__all__'

class AbnormalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbnormalUser
        fields = '__all__'