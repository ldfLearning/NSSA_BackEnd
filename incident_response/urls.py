from django.urls import path
from incident_response.api.warning import IncidentEventDetailAPIView, IncidentEventListAPIView,IncidentEventMonitorAPIView
from incident_response.api.email import EmailSettingsAPIView

urlpatterns = [
    path('warning', IncidentEventDetailAPIView.as_view()),
    path('warnings', IncidentEventListAPIView.as_view()),
    path('email_setting', EmailSettingsAPIView.as_view(), name='email_setting'),
    path('warning_monitor', IncidentEventMonitorAPIView.as_view(), name='warning_monitor'),
]