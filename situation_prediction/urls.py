from django.urls import path
from situation_prediction.views import SituationPredictionView, SituationPredictionHistoryView

urlpatterns = [
    path('value/', SituationPredictionView.as_view()),
    path('log/', SituationPredictionHistoryView.as_view()),

]