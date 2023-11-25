from django.urls import path
from api.traffic import AbnormalTrafficListAPIView, AbnormalTrafficDetailAPIView
from api.user import AbnormalUserListAPIView, AbnormalUserDetailAPIView

urlpatterns = [
    path('traffics', AbnormalTrafficListAPIView.as_view()),
    path('traffic', AbnormalTrafficDetailAPIView.as_view()),
    path('users', AbnormalUserListAPIView.as_view()),
    path('user', AbnormalUserDetailAPIView.as_view()),
]