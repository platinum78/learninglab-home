from django.urls import path

from . import views

app_name = "roster"

urlpatterns = [
    path('', views.index, name='index'),
]
