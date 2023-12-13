from django.urls import path
from situation_events.api import SituationAPI

app_name = 'situation_events'
urlpatterns = [
    path('list/',SituationAPI.SituationEventView.as_view()),
    path('item/',SituationAPI.SituationEventItemView.as_view()),
    path('itemtype/',SituationAPI.SituationEventItemTypeView.as_view()),
]  
