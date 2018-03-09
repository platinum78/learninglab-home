from django.urls import path

from . import views

app_name = "roster"

urlpatterns = [
    path('', views.index, name='index'),
    path('groups/', views.set_groups, name="groups"),
    path('groups/manual/', views.grouping_manual, name="grouping_manual"),
    path('groups/manual/post/', views.grouping_handler, name="grouping_handler"),
]
