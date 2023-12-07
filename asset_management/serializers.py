from rest_framework.serializers import ModelSerializer
from asset_management.models import AssetService

class AssetServiceSerializer(ModelSerializer):
    class Meta:
        model = AssetService
        fields = '__all__'