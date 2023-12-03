from rest_framework import serializers
from incident_response.models import IncidentEvent,EmailSettings

class IncidentEventSerializer(serializers.ModelSerializer): 
    class Meta:
        model = IncidentEvent
        fields = '__all__'

class EmailSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSettings
        fields = '__all__'