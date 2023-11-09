from django.urls import path, re_path

from asset_management.api.workshop import WorkshopBasicView, WorkshopToolView
from asset_management.api.productionline import ProductionlineBasicView
from asset_management.api.asset import AssetBasicView
from asset_management.api.assetservice import AssetServiceBasicView

urlpatterns = [
    path("workshop/", WorkshopBasicView.as_view()),
    re_path(r"workshop/(?P<pk>\d+)/", WorkshopToolView.as_view()),

    re_path("productionline", ProductionlineBasicView.as_view()),
    re_path("asset", AssetBasicView.as_view()),
    re_path("assetservice", AssetServiceBasicView.as_view()),
]
