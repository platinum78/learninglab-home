from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.template import loader, Context
from votes.models import *
from roster.models import *

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

import numpy as np
import os,sys
import cgi
import cgitb
cgitb.enable()
os.environ['HOME'] = '/tmp'

from votes.models import *
from roster.models import *
from courses.models import *

from collections import OrderedDict

# Create your views here.
def question_stats(request, question):
    c = Course.find_active_course()
    q = Question.objects.get(question_num=question)
    current_question_responses = Response.objects.filter(responder__enrolled_course=c, question=q)
    active_question_text = q.question_text
    choice_cnt = q.questionnaires_cnt
    choice_list = list(range(choice_cnt))
    first_vote = []
    second_vote = []
    for choice in range(choice_cnt):
        first_vote.append(len(current_question_responses.filter(answer_1=choice+1, responder__enrolled_course=c)))
        second_vote.append(len(current_question_responses.filter(answer_2=choice+1, responder__enrolled_course=c)))

    vote_dict = OrderedDict(zip(first_vote, second_vote))
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    fig = plt.figure(1, figsize=[8,6], tight_layout=True)
    plt.bar(np.arange(1, 1+choice_cnt)-0.125, first_vote, width=0.25, label="First Vote")
    plt.bar(np.arange(1, 1+choice_cnt)+0.125, second_vote, width=0.25, label="Second Vote")
    plt.xticks([0,1,2,3,4,5])
    plt.yticks(np.int32(np.arange(0, max(first_vote+second_vote)+1)))
    plt.title('Result for: %s' % active_question_text, fontsize=16)
    plt.legend()
    fig.savefig(BASE_DIR+'/static/plotImg/barplot.svg')
    fig.clear()

    context = {
        'first_vote': first_vote,
        'second_vote': second_vote,
        'fig_path': '/static/plotImg/barplot.svg',
        'active_question_text': active_question_text,
    }

    question_stats_html = loader.get_template('stats/question_stats.html')
    return HttpResponse(question_stats_html.render(context, request))

def select_date(request):
    year_range = list(range(2010, 2030))
    month_range = list(range(1, 13))
    day_range = list(range(1, 32))
    context = {
        'year_range': year_range,
        'month_range': month_range,
        'day_range': day_range,
    }
    date_select_html = loader.get_template("stats/select_date.html")
    return HttpResponse(date_select_html.render(context, request))

def select_date_handler(request):
    try:
        year = request.POST["year"]
        month = request.POST["month"]
        day = request.POST["day"]
        course = Course.objects.get(is_active=True)
    except:
        pass
    return redirect('/voting/stats/classreport/%s/%s/%s/' % (year, month, day))

def classreport(request, year, month, day):
    present_roster, absent_roster, present_rate = presence_check([year,month,day])
    present_cnt = len(present_roster)
    absent_cnt = len(absent_roster)
    classreport_html = loader.get_template("stats/classreport.html")
    context = {
        "present_roster": present_roster,
        "absent_roster": absent_roster,
        "present_cnt": present_cnt,
        "absent_cnt": absent_cnt,
        "present_rate": present_rate*100,
    }
    return HttpResponse(classreport_html.render(context, request))

def presence_check(date):
    # presence check screen
    year, month, day = date[0], date[1], date[2]
    course = Course.objects.get(is_active=True)
    full_roster = Student.objects.filter(enrolled_course=course)
    present_roster = []
    absent_roster = []
    present_rate = len(present_roster) / len(full_roster)
    time_range = [timezone.datetime(year,month,day,0,0), timezone.datetime(year,month,day,23,59)]
    for student in full_roster:
        if Response.objects.filter(timestamp__range=time_range, responder=student).count() != 0:
            present_roster.append(student)
        else:
            absent_roster.append(student)
    return present_roster, absent_roster, present_rate
