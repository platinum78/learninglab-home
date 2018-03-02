from django.urls import path

from . import views

app_name = "votes"

urlpatterns = [
    # Voting system homepage
    path('', views.index, name='index'),
    path('vote/', views.response, name='response'),
]
