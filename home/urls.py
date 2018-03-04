from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

app_name = 'home'
urlpatterns = [
    # homepage / login / logout
    ################################################################
    path('', views.index, name='homepage'),
    path('login/', views.login_, name='login'),
    path('logout/', views.logout_, name='logout'),
    path('user404/', views.user404, name='user404'),
    path('user404/tempregister/', views.visitor_handler, name="visitorhandler"),
    path('invalid_request/', views.invalid_request, name="invalid"),

    # student homepage / account info
    ################################################################
    path('student/', views.student, name='student'),
    path('student/accountinfo/', views.student_accountinfo, name="student_accountinfo"),
    path('student/accountinfo/changepassword/', views.student_change_password, name="student_change_password"),
    path('student/accountinfo/changepassword/parse/', views.student_password_handler, name="student_password_handler"),
    path('student/accountinfo/changepassword/error/', views.student_password_error, name="student_password_error"),
    path('student/accountinfo/changepassword/success/', views.student_password_success, name="student_password_success"),

    # faculty homepage / account info
    ################################################################
    path('faculty/', views.faculty, name='faculty'),
    path('faculty/selectcourse/', views.select_course, name="selectcourse"),
    path('faculty/selectcourse/parse/', views.course_selection_handler, name="course_selection_handler"),
    path('faculty/questionmonitor/', include('questionmonitor.urls')),
    path('faculty/sysstat/', views.sysstat, name="sysstat"),
    path('faculty/sysstat/classinit/selectfile/',
        views.roster_upload, name="roster_upload"),
    path('faculty/sysstat/classinit/send/',
        views.excel_upload_handler, name="excelsend"),
    path('faculty/sysstat/classinit/<str:filename>/preview/', views.excelpreview, name="excelpreview"),
    path('faculty/sysstat/classinit/parse/filename=<str:file_name>/', views.register_students_handler),
    path('faculty/sysstat/classinit/result/', views.student_registration_result, name="register_result"),
    path('faculty/sysstat/classinit/calibrate/', views.student_calibration, name="student_calibration"),
    path('faculty/sysstat/classinit/calibrated/', views.calibration_result, name="calibration_result"),

    # visitor homepage
    ################################################################
    path('visitor/', views.visitor, name="visitor"),

    # handler urls
    ################################################################
    path('accounterror/', views.accounterror, name="accounterror"),
    path('classreport/selectdateclass/', views.select_date_class, name="selectdateclass"),
    path('classreport/selectdateclass/select/', views.dateclass_redirect, name="parsedateclass"),
    path('classreport/date=<int:date>/class=<int:class_num>/', views.classreport),
    path('faculty/sysstat/classinit/calibrate/parse/', views.student_calibration_handler, name="student_calibration_handler"),
]
