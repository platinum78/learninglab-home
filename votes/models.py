from django.db import models
from roster.models import Student
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=2000)
    questionnaires_cnt = models.IntegerField(default=4, null=False)
    pub_date = models.DateTimeField('Date Published')
    question_state = models.IntegerField(default=0,
                                        validators=[MinValueValidator(0), MaxValueValidator(2)])
    lecture_num = models.IntegerField(default=0, null=False)
    question_num = models.IntegerField(default=0, null=False)

    def find_active(deactivate=False, calibrate=False):
        active_cnt = Question.objects.all().exclude(question_state=0).count()
        if active_cnt > 1:
            # more than one question is active currently, then.
            if calibrate == True:
                active_questions = Course.objects.filter(is_active=True)
                for question in active_questions:
                    question.is_active = False
                    question.save()
                raise Course.DoesNotExist
            pass
            pass
        elif active_cnt == 0:
            # no question is active currently, then.
            raise Question.DoesNotExist
        else:
            active_question = Question.objects.all().exclude(question_state=0)[0]
            if deactivate == False:
                return active_question
            else:
                active_question.question_state = 0
                active_question.save()
                raise Question.DoesNotExist

    def close_all():
        questions = Question.objects.all().exclude(question_state=0)
        for question in questions:
            question.question_state = 0
            question.save()


class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_1 = models.IntegerField(default=0)
    answer_2 = models.IntegerField(default=0)
    responder = models.ForeignKey(Student, on_delete=models.CASCADE)

# utility functions
################################################


def question_initialization(lecture_cnt, question_cnt):
    Question.objects.all().delete()
    for lecture in range(lecture_cnt):
        for question in range(question_cnt):
            Question.objects.create(question_text="Problem %d | Lecture %d" %
                                    (question+1, lecture+1), question_state=0,
                                    lecture_num=lecture+1,
                                    question_num=question+1,
                                    pub_date=timezone.now())
