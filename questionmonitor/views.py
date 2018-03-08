from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.template import loader, Context
from votes.models import *
from roster.models import *
from courses.models import *
from django.contrib.auth.models import User, AnonymousUser
from collections import OrderedDict

# Create your views here.

def index(request):
    # reject request if not affiliated to instructor group
    ############################################################
    try:
        user = request.user
        Faculty.objects.get(user=user)
    except Faculty.DoesNotExist:
        return HttpResponseForbidden("FORBIDDEN: You're not authorized to view this page.")

    course = Course.objects.get(is_active=True)

    try:
        active_question = Question.find_active()
        active_question_text = active_question.question_text
        question_state = active_question.question_state
        active_question_link = "/voting/questionmonitor/%d/state/" % active_question.question_num
    except Question.DoesNotExist:
        active_question_text = 'None'
        question_state = 0
        active_question_link = ""

    # find number of quesetions
    questionquery = Question.objects.all().order_by("question_num")
    has_response = OrderedDict()
    for question in questionquery:
        try:
            Response.objects.get(course=course, question=question)
            has_response[question.question_num] = True
        except Response.DoesNotExist:
            has_response[question.question_num] = False
    index_html = loader.get_template('questionmonitor/question_num.html')
    num = list(range(Question.objects.all().count()))
    context = {
        'active_question_text': active_question_text,
        'question_state': question_state,
        'active_question_link': active_question_link,
        'questions': questionquery,
        'question_info': has_response.items(),
    }
    return HttpResponse(index_html.render(context, request))

def killswitch(request):
    try:
        Question.find_active(deactivate=True)
    except Question.DoesNotExist:
        return redirect("questionmonitor:index")

def show_state(request, question_num):
    state_html = loader.get_template('questionmonitor/show_state.html')
    q = Question.objects.get(question_num=question_num)
    question_state = q.question_state
    context = {
        'question_num': question_num,
        'question_state': question_state,
    }
    return HttpResponse(state_html.render(context, request))
    pass

def question_to_first_vote(request, question_num):
    try:
        q = Question.find_active(deactivate=True)
    except Question.DoesNotExist:
        q = Question.objects.get(question_num=question_num)
        q.question_state = 1
        q.save()
    return redirect("/voting/faculty/questionmonitor/%d/state/" % question_num)

def question_to_second_vote(request, question_num):
    try:
        q = Question.find_active(deactivate=True)
    except Question.DoesNotExist:
        q = Question.objects.get(question_num=question_num)
        q.question_state = 2
        q.save()
    return redirect("/voting/faculty/questionmonitor/%d/state/" % question_num)

def question_deactivate(request, question_num):
    try:
        q = Question.find_active(deactivate=True)
    except Question.DoesNotExist:
        q = Question.objects.get(question_num=question_num)
        q.question_state = 0
        q.save()
    return redirect("/voting/faculty/questionmonitor/%d/state/" % question_num)
