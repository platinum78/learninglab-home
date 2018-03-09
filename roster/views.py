from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import Context, loader

from roster.models import *
from courses.models import *

# Create your views here.
def index(request):
    # return HttpResponse("Welcome! You're in the roster index page.")
    course = Course.objects.get(is_active=True)
    full_roster = Student.objects.filter(enrolled_course=course)
    index_html = loader.get_template('roster/index.html')
    context = {
        "full_roster": full_roster,
    }
    return HttpResponse(index_html.render(context, request))

def set_groups(request):
    groups_html = loader.get_template("roster/set_groups.html")
    context = {}
    return HttpResponse(groups_html.render(context, request))

def grouping_manual(request):
    grouping_manual_html = loader.get_template("roster/grouping_manual.html")
    course = Course.objects.get(is_active=True)

    full_roster = Student.objects.filter(enrolled_course=course)
    names = []
    student_numbers = []
    for student in full_roster:
        names.append(student.name_text_korean)
        student_numbers.append(student.id_text)

    context = {
        # "names": names,
        # "student_numbers": student_numbers,
        # "students": list(range(len(full_roster))),
        "course_title": course.title(),
        "full_roster": full_roster,
    }
    return HttpResponse(grouping_manual_html.render(context, request))

def grouping_handler(request):
    for student in Student.objects.all():
        student.group_num = request.POST[student.id_text]
        student.save()
    return HttpResponse("Group addition finished!")
