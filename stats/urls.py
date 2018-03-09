from django.urls import path, include
from . import views

app_name = 'stats'
urlpatterns = [
    # url patterns for voting statistics
    path('question_stats/<int:question>/', views.question_stats, name="question_stats"),

    # url patterns for class report
    # path('classreport/', views.classreport, name="classreport"),
    path('classreport/selectdateclass/', views.select_date, name="select_date"),
    path('classreport/selectdateclass/post/', views.select_date_handler, name="select_date_handler"),
    path('classreport/<int:year>/<int:month>/<int:day>/', views.classreport),
]
