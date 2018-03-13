from django.db import models
from django.contrib.auth.models import User
# from roster.models import Student

"""
Each class in models module in Django projects corresponds to tables. The name
of the class will be the name of table, and the class members will be the field
of that table.
"""
# Create your models here.


class Course(models.Model):
    course_name = models.CharField(max_length=50, null=False)
    # Course name should include only the name of course.
    # i.e. Engineering Mathematics (or EM)

    class_num = models.IntegerField(null=False, default=0)
    # Class number should be an integer.

    semester = models.IntegerField(null=False, default=0)
    # Semester should be either 1 or 2.
    # If this system is needed for summer or winter semester, one should update
    # this field into models.CharField()

    year = models.IntegerField(null=False, default=0)
    # The year when the course is opened.

    course_token = models.CharField(null=True, unique=True, max_length=15, default="0")
    # Course token is a kind of shortcut to find the course easily.
    # Each course will get an unique token, and this token will be generated
    # automatically. Therefore, DO NOT use objects.create()

    is_active = models.BooleanField(null=False, default=False)
    # is_active shows the status of the course.
    # Only one course will have is_active == True, since only one course can be
    # held in a classroom.

    roster_filename = models.CharField(null=True, default=None, max_length=100)
    # This originally was made to connect the roster .xlsx files with each
    # course. This function is not needed currently, but keep it; it might be
    # needed later on.

    # This function automatically generates formatted course title/
    # Ex) "2018-1 EM Class 41"
    def title(self):
        text = str(self.year) + "-" + str(self.semester) + " " + str(self.course_name) + " - Class " + str(self.class_num)
        return text

    # This functions looks for active course. If more than one, it deactivates
    # everything, since it is an error. If there is no active course, it raises
    # DoesNotExist error message. DoesNotExist is an error message indicating
    # there is not matching query in the table, and is used like
    # (Model Name).DoesNotExist - Ex) Student.DoesNotExist
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

    # Closes (all) active function. This function is used for troubleshooting
    # multiple-active-courses case or when the instructor logs out from the system.
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
