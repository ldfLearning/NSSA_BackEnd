from django.urls import path
from incident_response.views import IncidentEventDetailAPIView, IncidentEventListAPIView

urlpatterns = [
    path('event', IncidentEventDetailAPIView.as_view()),
    path('events', IncidentEventListAPIView.as_view())
]