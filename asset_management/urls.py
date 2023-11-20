from django.urls import path

from asset_management.api.workshop import WorkshopBasicView
from asset_management.api.workshopfile import WorkshopFileView
from asset_management.api.productionline import ProductionlineBasicView
from asset_management.api.productionlinefile import ProductionlineFileView
from asset_management.api.asset import AssetBasicView
from asset_management.api.assetfile import AssetFileView
from asset_management.api.assetservice import AssetServiceBasicView
from asset_management.api.hostscan import AssetScan
from asset_management.api.jtopojson import JtopoView
from asset_management.api.jtopoasset import JtopoAssetView
from asset_management.api.jtopoauto import JtopoAutoView


# 千万不能把path换成re_path，因为re_path是只要下面的字符串存在于url中即可，而path是必须完全匹配
urlpatterns = [
    path("workshop/", WorkshopBasicView.as_view()),  # 车间信息表基本增删改查
    path("workshopfile/", WorkshopFileView.as_view()),  # 车间信息表文件导入导出

    path("productionline/", ProductionlineBasicView.as_view()),  # 产线信息表基本增删改查
    path("productionlinefile/", ProductionlineFileView.as_view()),  # 产线信息表文件导入导出

    path("asset/", AssetBasicView.as_view()),  # 资产信息表基本增删改查
    path("assetfile/", AssetFileView.as_view()),  # 资产信息表文件导入导出

    path("assetservice/", AssetServiceBasicView.as_view()),  # 资产服务信息表基本增删改查

    path("assetscan/", AssetScan.as_view()),  # 资产和服务扫描

    path("jtopo/", JtopoView.as_view()),  # 与前端交互网络拓扑json数据
    path("jtopo/asset/", JtopoAssetView.as_view()),  # 与前端交互网络拓扑json数据
    path("jtopo/auto/", JtopoAutoView.as_view()),  # 自动生成拓扑图
]
