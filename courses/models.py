from django.db import models
from django.contrib.auth.models import User
# from roster.models import Student

# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=50, null=False)
    class_num = models.IntegerField(null=False, default=0)
    semester = models.IntegerField(null=False, default=0)
    year = models.IntegerField(null=False, default=0)
    course_token = models.CharField(null=True, unique=True, max_length=15, default="0")
    is_active = models.BooleanField(null=False, default=False)
    roster_filename = models.CharField(null=True, default=None, max_length=100)

    def title(self):
        text = str(self.year) + "-" + str(self.semester) + " " + str(self.course_name) + " - Class " + str(self.class_num)
        return text

    def find_active_course(deactivate=False):
        active_cnt = len(Course.objects.filter(is_active=True))
        if active_cnt > 1:
            # more than one question is active currently, then.
            if deactivate == True:
                active_questions = Course.objects.filter(is_active=True)
                for question in active_questions:
                    question.is_active = False
                    question.save()
                raise Course.DoesNotExist
            pass
        elif active_cnt == 0:
            # no question is active currently, then.
            raise Course.DoesNotExist
        else:
            active_course = Course.objects.get(is_active=True)
            if deactivate == False:
                return active_course
            else:
                active_course.question_state = False
                active_course.save()
                raise Course.DoesNotExist

    def close_all():
        courses = Course.objects.filter(is_active=True)
        for course in courses:
            course.is_active = False
            course.save()
        # visitors = Student.objects.filter(is_visitor=True)
        # visitor_users = []
        # for visitor in visitors:
        #     visitor_users.append(visitor.user)
        # for visitor_user in visitor_users:
        #     visitor_user.delete()
