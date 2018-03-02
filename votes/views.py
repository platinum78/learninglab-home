from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import Context, loader
from .models import *
from courses.models import *
from roster.models import Student
from django.contrib.auth.models import User


# Create your views here.
################################################
def index(request):
    current_user = request.user
    try:
        active_course = Course.objects.get(is_active=True)

        try:
            Student.objects.get(user=current_user, enrolled_course=active_course)
            is_in_current_class = True

            try:
                active_question = Question.find_active()
                active_question_text = active_question.question_text
                active_questionnaires_cnt = active_question.questionnaires_cnt
                active_question_choice_range = list(range(1,active_question.questionnaires_cnt+1))
                pane_width = 100 / active_questionnaires_cnt
                question_state = active_question.question_state
            except Question.DoesNotExist:
                active_question_text = 'None'
                active_questionnaires_cnt = 0
                active_question_choice_range = []
                pane_width = 100
                question_state = 0

        except Student.DoesNotExist:
            is_in_current_class = False
            active_question_text = 'None'
            active_questionnaires_cnt = 0
            active_question_choice_range = []
            pane_width = 100
            question_state = 0

    except Course.DoesNotExist:
        is_in_current_class = False
        active_question_text = 'None'
        active_questionnaires_cnt = 0
        active_question_choice_range = []
        pane_width = 100
        question_state = 0




    html = loader.get_template('votes/index.html')
    context = {
        'active_question_text': active_question_text,
        'active_question_choice_cnt': active_questionnaires_cnt,
        'active_question_choice_range': list(range(1,active_questionnaires_cnt+1)),
        'pane_width': pane_width,
        'question_state': question_state,
        'is_in_current_class': is_in_current_class,
    }
    return HttpResponse(html.render(context, request))


# voting actions
################################################
def response(request):
    q = Question.find_active()
    selected_choice = request.POST['choice']

    if request.user.is_authenticated != True:
        # make some exception handling methods,
        return Http404('Not authenticated')
    else:
        current_user = request.user
        current_student = Student.objects.get(user=current_user)
        current_iteration = q.question_state
        if current_iteration == 1:
            try:
                r = Response.objects.get(question=q, responder=current_student)
                r.answer_1 = selected_choice
                r.save()
            except Response.DoesNotExist:
                Response.objects.create(question=q, answer_1=selected_choice,
                                        responder=current_student)
        elif current_iteration == 2:
            try:
                r = Response.objects.get(question=q, responder=current_student)
                r.answer_2 = selected_choice
                r.save()
            except Response.DoesNotExist:
                Response.objects.create(question=q, answer_2 = selected_choice,
                                        responder=current_student)
        return redirect('home:student')
