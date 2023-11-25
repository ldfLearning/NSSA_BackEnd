from rest_framework import serializers
from abnormal_attack.models import AbnormalTraffic, AbnormalHost


class AbnormalTrafficSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbnormalTraffic
        fields = '__all__'


class AbnormalHostSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbnormalHost
        fields = '__all__'
