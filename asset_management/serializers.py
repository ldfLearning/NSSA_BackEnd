from rest_framework.serializers import ModelSerializer
from asset_management.models import Workshop, Productionline, Asset, AssetService


class WorkshopSerializer(ModelSerializer):
    class Meta:
        model = Workshop
        fields = '__all__'


class ProductionlineSerializer(ModelSerializer):
    class Meta:
        model = Productionline
        fields = '__all__'


class AssetSerializer(ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'


class AssetServiceSerializer(ModelSerializer):
    class Meta:
        model = AssetService
        fields = '__all__'
from rest_framework.serializers import ModelSerializer
from asset_management.models import AssetService

class AssetServiceSerializer(ModelSerializer):
    class Meta:
        model = AssetService
        fields = '__all__'