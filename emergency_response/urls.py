from django.urls import path
from .api.email import EmailUpdateAPIView
from .api.warning import WarningMonitorAPIView

app_name = 'emergency_response'
urlpatterns = [
    path('update_email', EmailUpdateAPIView.as_view(), name='update_email'),
    path('warning_monitor', WarningMonitorAPIView.as_view(), name='warning_monitor'),
]