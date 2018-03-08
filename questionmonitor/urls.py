from django.urls import path, include
from . import views

app_name = 'questionmonitor'
urlpatterns = [
    path('', views.index, name="index"),
    path('killswitch/', views.killswitch, name="killswitch"),
    path('<int:question_num>/state/', views.show_state, name="state"),
    path('<int:question_num>/firstvote/', views.question_to_first_vote, name="first_vote"),
    path('<int:question_num>/secondvote/', views.question_to_second_vote, name="second_vote"),
    path('<int:question_num>/deactivate/', views.question_deactivate, name="deactivate"),
]
