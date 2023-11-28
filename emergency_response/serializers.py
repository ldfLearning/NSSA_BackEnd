from rest_framework import serializers
from emergency_response.models import AbnormalWarning,EmailSettings

class AbnormalWarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbnormalWarning
        fields = '__all__'

class EmailSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSettings
        fields = '__all__'