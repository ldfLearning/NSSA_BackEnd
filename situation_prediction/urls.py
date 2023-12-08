from django.urls import path
from .api.situation import SituationPredictionView, SituationPredictionHistoryView

urlpatterns = [
    path('value/', SituationPredictionView.as_view()),
    path('log/', SituationPredictionHistoryView.as_view()),

]