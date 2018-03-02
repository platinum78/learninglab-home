from django.shortcuts import render
from django.http import HttpResponse
from matplotlib import pyplot as plt
from django.template import loader, Context
from votes.models import *
from roster.models import *
import numpy as np
import os

# Create your views here.
def index(request, lecture, question):
    c = find_active_course()
    q = Question.objects.get(lecture_num=lecture, question_num=question)
    current_question_responses = Response.objects.filter(responder__enrolled_course=c, question=q)
    active_question_text = q.question_text
    choice_cnt = q.questionnaires_cnt
    first_vote = []
    second_vote = []
    for choice in range(choice_cnt):
        first_vote.append(len(current_question_responses.filter(answer_1=choice+1, responder__enrolled_course=c)))
        second_vote.append(len(current_question_responses.filter(answer_2=choice+1, responder__enrolled_course=c)))

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
        'fig_path': '/static/plotImg/barplot.svg',
        'active_question_text': active_question_text,
    }

    stats_html = loader.get_template('stats/index.html')
    return HttpResponse(stats_html.render(context, request))

def select_question(request):
    return HttpResponse('Question selection page.')
