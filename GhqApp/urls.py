from django.urls import path
from .views import QuestionDisplayView, ResultView

app_name = 'ghq_app'

urlpatterns = [ 
    path('questions/', QuestionDisplayView.as_view(), name='questions'),
    path('result/<str:quiz_taken>/',ResultView.as_view(), name='result')
]