from django.urls import re_path as url

from asset_management.views import add_workshop

urlpatterns = [
    url("add_workshop", add_workshop, ),
]

