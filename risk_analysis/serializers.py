from rest_framework import serializers
from risk_analysis.models import AssetRisk

class AssetRiskSerializer(serializers.ModelSerializer): 
    class Meta:
        model = AssetRisk
        fields = '__all__'