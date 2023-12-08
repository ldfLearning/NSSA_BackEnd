from django.urls import path
from risk_analysis.api.risk import RiskAPIView,RiskCalculationAPIView


app_name = 'risk_analysis'
urlpatterns = [
    path('risk', RiskAPIView.as_view(), name='get_risk'),
    path('cal', RiskCalculationAPIView.as_view(), name='cal_risk'),
]