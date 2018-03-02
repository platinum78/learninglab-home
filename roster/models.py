from django.db import models
from django.contrib.auth.models import User
import pandas
import numpy as np
from courses.models import *

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                null=True, default=None)
    id_text = models.CharField(max_length=10, primary_key=True)
    name_text_korean = models.CharField(max_length=20)
    name_text_english = models.CharField(max_length=30)
    class_num= models.IntegerField(default=0)
    major_text = models.CharField(max_length=30)
    grade = models.IntegerField(default=0)
    prev_gpa = models.FloatField(default=0)
    enrolled_course = models.ManyToManyField(Course)
    is_visitor = models.BooleanField(default=False)

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                null=True, default=None)
    id_text = models.CharField(max_length=10, primary_key=True)
    name_text_korean = models.CharField(max_length=20)
    name_text_english = models.CharField(max_length=30)
    class_num= models.IntegerField(default=0)
    position_text = models.IntegerField(default=0)

class Visitor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                null=True, default=None)
    id_text = models.CharField(max_length=10, primary_key=True)
    temp_password = models.CharField(max_length=15, default = "")

def student_batch_addition(sheet_path, year, semester, course_name, class_num):
    data = pandas.read_excel(sheet_path, sheet_name='sheet').as_matrix()
    student_cnt = data.shape[0]
    course = Course.objects.get(year=year, semester=semester, course_name=course_name,
                                class_num=class_num)

    for idx in range(student_cnt):
        user = User.objects.create_user(username=str(data[idx,3]),
                                        password=str(data[idx,3]),
                                        email=data[idx,6],
                                        first_name=data[idx,4])

        student = Student.objects.create(user=user, id_text=data[idx,3],
                                        name_text_korean=data[idx,5],
                                        name_text_english=data[idx,4],
                                        class_num=class_num,
                                        major_text=data[idx,1],
                                        grade=data[idx,2])
        student.enrolled_course.add(course)
        student.save()
