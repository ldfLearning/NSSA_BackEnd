from django.urls import path
from .api.risk import RiskAnalysisAPIView


app_name = 'risk_analysis'
urlpatterns = [
    path('analysis', RiskAnalysisAPIView.as_view(), name='risk_analysis'),
]