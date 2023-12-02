from django.urls import path
from situation_prediction.views import SituationPredictionView
urlpatterns = [
    path('value/', SituationPredictionView.as_view()),
]