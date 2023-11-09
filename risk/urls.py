from django.urls import path
from .api.RiskAnalysis import RiskAnalysisAPIView


app_name = 'risk'
urlpatterns = [
    path('analysis/', RiskAnalysisAPIView.as_view(), name='risk_analysis'),
]
