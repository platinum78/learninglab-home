from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.template import loader, Context
from votes.models import *
from roster.models import *
from django.contrib.auth.models import User, AnonymousUser

# Create your views here.
def index(request):
    # reject request if not affiliated to instructor group
    ############################################################
    try:
        user = request.user
        Faculty.objects.get(user=user)
    except Faculty.DoesNotExist:
        return HttpResponseForbidden("FORBIDDEN: You're not authorized to view this page.")

    try:
        active_question = Question.find_active()
        active_question_text = active_question.question_text
        question_state = active_question.question_state
        active_question_link = "/questionmonitor/%d/%d/state/" % (active_question.lecture_num, active_question.question_num)
    except Question.DoesNotExist:
        active_question_text = 'None'
        question_state = 0
        active_question_link = ""

    # find number of lectures
    lectures_cnt = Question.objects.order_by('-lecture_num')[0].lecture_num

    index_html = loader.get_template('questionmonitor/index.html')
    context = {
        'active_question_text': active_question_text,
        'lectures': list(range(lectures_cnt)),
        'question_state': question_state,
        'active_question_link': active_question_link,
    }
    return HttpResponse(index_html.render(context, request))

def killswitch(request):
    try:
        Question.find_active(deactivate=True)
    except Question.DoesNotExist:
        return redirect("questionmonitor:index")

def qlist(request, lecture_num):
    this_lecture_questions = Question.objects.filter(lecture_num=lecture_num)
    this_lecture_questions = this_lecture_questions.order_by("question_num")

    try:
        active_question = Question.find_active()
        active_question_text = active_question.question_text
        question_state = active_question.question_state
        active_question_link = "/questionmonitor/%d/%d/state/" % (active_question.lecture_num, active_question.question_num)
    except Question.DoesNotExist:
        active_question_link = ""
        active_question_text = 'None'
        question_state = 0

    qlist_html = loader.get_template('questionmonitor/qlist.html')
    context = {
        'active_question_text': active_question_text,
        'this_lecture_questions': this_lecture_questions,
        'lecture_num': lecture_num,
        'question_state': question_state,
        'active_question_link': active_question_link,
    }
    return HttpResponse(qlist_html.render(context, request))

def show_state(request, lecture_num, question_num):
    state_html = loader.get_template('questionmonitor/show_state.html')
    q = Question.objects.get(lecture_num=lecture_num, question_num=question_num)
    question_state = q.question_state
    context = {
        'lecture_num': lecture_num,
        'question_num': question_num,
        'question_state': question_state,
    }
    return HttpResponse(state_html.render(context, request))
    pass

def question_to_first_vote(request, lecture_num, question_num):
    try:
        q = Question.find_active(deactivate=True)
    except Question.DoesNotExist:
        q = Question.objects.get(lecture_num=lecture_num, question_num=question_num)
        q.question_state = 1
        q.save()
    return redirect("/faculty/questionmonitor/%d/%d/state/" % (lecture_num, question_num))

def question_to_second_vote(request, lecture_num, question_num):
    try:
        q = Question.find_active(deactivate=True)
    except Question.DoesNotExist:
        q = Question.objects.get(lecture_num=lecture_num, question_num=question_num)
        q.question_state = 2
        q.save()
    return redirect("/faculty/questionmonitor/%d/%d/state/" % (lecture_num, question_num))

def question_deactivate(request, lecture_num, question_num):
    try:
        q = Question.find_active(deactivate=True)
    except Question.DoesNotExist:
        q = Question.objects.get(lecture_num=lecture_num, question_num=question_num)
        q.question_state = 0
        q.save()
    return redirect("/faculty/questionmonitor/%d/%d/state/" % (lecture_num, question_num))
