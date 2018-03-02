from django.urls import path, include
from . import views

app_name = 'stats'

urlpatterns = [
    path('<int:lecture>/<int:question>/', views.index, name="index"),
    path('selectquestion/', views.select_question, name="selectquestion"),
]
