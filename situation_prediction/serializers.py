from rest_framework import serializers

from situation_prediction.models import Situation


class SituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Situation
        fields = '__all__'
