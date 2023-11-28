from django.urls import path
from .api.flow import FlowAPIView
from .api.threat import ThreatAPIView

app_name = 'flow_monitoring'
urlpatterns = [
    path('flow', FlowAPIView.as_view(), name='get_flow'),
    path('threat', ThreatAPIView.as_view(), name='get_threat'),
]