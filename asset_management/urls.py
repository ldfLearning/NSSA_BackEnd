from django.urls import path, re_path

from asset_management.api.workshop import WorkshopBasicView
from asset_management.api.productionline import ProductionlineBasicView
from asset_management.api.asset import AssetBasicView
from asset_management.api.assetservice import AssetServiceBasicView

urlpatterns = [
    path("workshop/", WorkshopBasicView.as_view()),
    # re_path(r"workshop/(?P<pk>\d+)/", WorkshopToolView.as_view()),

    path("productionline/", ProductionlineBasicView.as_view()),
    # re_path(r"productionline/(?P<pk>\d+)/", ProductionlineToolView.as_view()),

    path("asset/", AssetBasicView.as_view()),
    # re_path(r"asset/(?P<pk>\d+)/", AssetToolView.as_view()),

    path("assetservice/", AssetServiceBasicView.as_view()),
    # re_path(r"assetservice/(?P<pk>\d+)/", AssetServiceToolView.as_view()),
]
