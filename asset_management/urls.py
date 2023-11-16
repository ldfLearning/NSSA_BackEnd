from django.urls import re_path

from asset_management.api.workshop import WorkshopBasicView
from asset_management.api.productionline import ProductionlineBasicView
from asset_management.api.asset import AssetBasicView
from asset_management.api.assetservice import AssetServiceBasicView
from asset_management.api.hostscan import HostScan


urlpatterns = [
    re_path("workshop/", WorkshopBasicView.as_view()),

    re_path("productionline/", ProductionlineBasicView.as_view()),

    re_path("asset/", AssetBasicView.as_view()),

    re_path("assetservice/", AssetServiceBasicView.as_view()),

    re_path("hostscan/", HostScan.as_view()),

]
