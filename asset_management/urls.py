from django.urls import path

from asset_management.api.assetservice import AssetServiceBasicView

urlpatterns = [
    path("assetservice/", AssetServiceBasicView.as_view()),  # 资产服务信息表基本增删改查
]