from rest_framework import serializers
from abnormal_attack.models import AbnormalTraffic, AbnormalHost, AbnormalUser


class AbnormalTrafficSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbnormalTraffic
        fields = '__all__'

class AbnormalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbnormalUser
        fields = '__all__'

class AbnormalHostSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbnormalHost
        fields = '__all__'
