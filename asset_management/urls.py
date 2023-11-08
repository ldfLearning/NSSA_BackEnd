from django.conf.urls import url

from asset_management.views import add_workshop

urlpatterns = [
    url("add_workshop", add_workshop, ),
]

