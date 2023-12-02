from rest_framework import serializers
from incident_response.models import IncidentEvent

class IncidentEventSerializer(serializers.ModelSerializer): 
    class Meta:
        model = IncidentEvent
        fields = '__all__'