from django.urls import re_path

from asset_management.api.workshop import WorkshopBasicView
from asset_management.api.workshopfile import WorkshopFileView
from asset_management.api.productionline import ProductionlineBasicView
from asset_management.api.productionlinefile import ProductionlineFileView
from asset_management.api.asset import AssetBasicView
from asset_management.api.assetfile import AssetFileView
from asset_management.api.assetservice import AssetServiceBasicView
from asset_management.api.hostscan import AssetScan


urlpatterns = [
    re_path("workshop/", WorkshopBasicView.as_view()),  # 车间信息表基本增删改查
    re_path("workshopfile/", WorkshopFileView.as_view()),  # 车间信息表文件导入导出

    re_path("productionline/", ProductionlineBasicView.as_view()),  # 产线信息表基本增删改查
    re_path("productionlinefile/", ProductionlineFileView.as_view()),  # 产线信息表文件导入导出

    re_path("asset/", AssetBasicView.as_view()),  # 资产信息表基本增删改查
    re_path("assetfile/", AssetFileView.as_view()),  # 资产信息表文件导入导出

    re_path("assetservice/", AssetServiceBasicView.as_view()),  # 资产服务信息表基本增删改查

    re_path("assetscan/", AssetScan.as_view()),  # 资产和服务扫描

]
