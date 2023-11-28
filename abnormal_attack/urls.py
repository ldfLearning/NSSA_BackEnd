from django.urls import path

from abnormal_attack.api.user import AbnormalUserListAPIView, AbnormalUserDetailAPIView
from abnormal_attack.api.host import AbnormalHostListAPIView, AbnormalHostDetailAPIView
from abnormal_attack.api.traffic import AbnormalTrafficListAPIView, AbnormalTrafficDetailAPIView

urlpatterns = [
    path('traffics', AbnormalTrafficListAPIView.as_view()),
    path('traffic', AbnormalTrafficDetailAPIView.as_view()),
    path('users', AbnormalUserListAPIView.as_view()),
    path('user', AbnormalUserDetailAPIView.as_view()),
    path('hosts', AbnormalHostListAPIView.as_view()),
    path('host', AbnormalHostDetailAPIView.as_view()),
]