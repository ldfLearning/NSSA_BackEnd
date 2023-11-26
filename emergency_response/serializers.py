from rest_framework import serializers
from emergency_response.models import AbnormalWarning

class AbnormalWarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbnormalWarning
        fields = '__all__'
