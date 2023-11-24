from django.urls import path
from abnormal_attack.api.traffic import AbnormalTrafficListAPIView, AbnormalTrafficDetailAPIView

urlpatterns = [
    path('traffics', AbnormalTrafficListAPIView.as_view()),
    path('traffic', AbnormalTrafficDetailAPIView.as_view()),
]
