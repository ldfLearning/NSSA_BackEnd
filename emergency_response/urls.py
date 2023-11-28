from django.urls import path
from .api.email import EmailSettingsAPIView,EmailSendAPIView
from .api.warning import WarningMonitorAPIView,WarningListAPIView,WarningDetailAPIView

app_name = 'emergency_response'
urlpatterns = [
    path('email_setting', EmailSettingsAPIView.as_view(), name='email_setting'),
    path('send_email',EmailSendAPIView.as_view(),name='send_email'),
    path('warning_monitor', WarningMonitorAPIView.as_view(), name='warning_monitor'),
    path('warnings',WarningListAPIView.as_view()),
    path('warning',WarningDetailAPIView.as_view()),
]