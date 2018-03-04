from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.template import loader, Context
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, AnonymousUser
from django.core.files.storage import FileSystemStorage
from collections import OrderedDict

from .forms import *
from roster.models import *
from courses.models import *
from votes.models import *
import datetime, os, pandas, string, random
# from somewhere import handle_uploaded_file

# Create your views here.
def index(request):
    context = {}
    if request.user != AnonymousUser():
        try:
            Student.objects.get(user=request.user)
            return redirect("home:student")
        except Student.DoesNotExist:
            pass

        try:
            Faculty.objects.get(user=request.user)
            return redirect("home:faculty")
        except Faculty.DoesNotExist:
            raise Http404("No matching user!")

    homepage_html = loader.get_template('home/index_login.html')
    return HttpResponse(homepage_html.render(context, request))

def student(request):
    try:
        student_html = loader.get_template('home/student.html')
        user = request.user
        student_name = Student.objects.get(user=user).name_text_english
        context = {
            'student_name': student_name,
        }
        return HttpResponse(student_html.render(context, request))
    except Student.DoesNotExist:
        return redirect("home:invalid")

def faculty(request):
    try:
        Faculty.objects.get(user=request.user)
        # if the faculty forgot to logout previously, but somehow
        # there is no course active, he/she should be redirected
        # to the course selection page.
        ################################################################
        try:
            course = Course.objects.get(is_active=True)
        except Course.DoesNotExist:
            return redirect("home:selectcourse")

        # load class information from courses.models.Course model
        ################################################################
        course_name = course.course_name
        class_num = course.class_num
        course_title = str(course.year)+'-'+str(course.semester)+' '+course.course_name + " - Class " + str(course.class_num)

        # parse context and html template to the client
        ################################################################
        faculty_html = loader.get_template('home/faculty.html')
        user = request.user
        instructor_name = Faculty.objects.get(user=user).name_text_english
        context = {
            'instructor_name': instructor_name,
            'course_name': course_name,
            'course_year': course.year,
            'course_semester': course.semester,
            'class_num': class_num,
            'course_title': course_title,
        }
        return HttpResponse(faculty_html.render(context, request))
    except Faculty.DoesNotExist:
        return redirect("home:invalid")

def visitor(request):
    try:
        Student.objects.get(user=request.user)
        visitor_html = loader.get_template('home/visitor.html')
        user = request.user
        context = {}
        return HttpResponse(visitor_html.render(context, request))
    except Student.DoesNotExist:
        return redirect("home:invalid")

def invalid_request(request):
    invalid_request_html = loader.get_template('registration/invalid_request.html')
    context = {}
    return HttpResponse(invalid_request_html.render(context, request))

def student_accountinfo(request):
    # find the student info from roster.models.Student model
    ################################################################
    try:
        # find the student from the database
        user_id = request.user.username
        current_student = Student.objects.get(user=request.user)
        student_id = current_student.id_text
        name_english = current_student.name_text_english
        name_korean = current_student.name_text_korean
    except Student.DoesNotExist:
        # handle exception raised from absence of student info
        # make code for error message,
        pass # for now.

    # parse context and html template to the client
    ################################################################
    context = {
        'user_id': user_id,
        'student_id': student_id,
        'name_english': name_english,
        'name_korean': name_korean,
    }
    student_accountinfo_html = loader.get_template('home/student_accountinfo.html')
    return HttpResponse(student_accountinfo_html.render(context, request))

#@csrf_exempt
def login_(request):
    user_id = request.POST['userid']
    user_pw = request.POST['userpw']
    user = authenticate(username=user_id, password=user_pw)
    if user is not None:
        login(request, user)
    else:
        return redirect("home:user404")

    try:
        Student.objects.get(user=user)
        return redirect("home:student")
    except Student.DoesNotExist:
        pass

    try:
        Faculty.objects.get(user=user)
        return redirect("home:selectcourse")
    except Faculty.DoesNotExist:
        return redirect("home:user404")

def logout_(request):
    # deactivate all courses and questions, if the instructor logs out
    ################################################################
    logout_user = request.user
    try:
        Faculty.objects.get(user=logout_user)
        Question.close_all()
        Course.close_all()
        is_faculty = True
    except Faculty.DoesNotExist:
        is_faculty = False

    # log-out the user
    ################################################################
    logout(request)
    logout_html = loader.get_template('home/logged_out.html')
    context = {
        "is_faculty": is_faculty,
    }
    return HttpResponse(logout_html.render(context, request))

def user404(request):
    context = {}
    user404_html = loader.get_template('registration/user404.html')
    return HttpResponse(user404_html.render(context, request))

def visitor_handler(request):
    # create 15-digit arbitrary password
    charbank = string.ascii_uppercase + string.ascii_lowercase + string.digits
    random_pw = "".join(random.choice(charbank) for _ in range(15))
    user_id = request.POST["id"]

    # get temporary user data and add to visitor list
    user = User.objects.create_user(username=str(user_id),
                                    password=str(user_id))
    visitor = Student.objects.create(user=user,
                                    id_text=user_id)

    user_login = authenticate(usrename=user_id, password=random_pw)

    if user_login is not None:
        login(request, user_login)
    return redirect("home:visitor")

def anonymoususer_logout(request):
    user = request.user
    user.logout(request)
    user.delete()

def sysstat(request):
    # load
    sysstat_html = loader.get_template('home/sysstat.html')
    context = {}
    return HttpResponse(sysstat_html.render(context, request))

def accounterror(request):
    context = {}
    accounterror_html = loader.get_template("registration/accounterror.html")
    return HttpResponse(accounterror_html.render(context, request))

def select_date_class(request):
    year_range = list(range(2010, 2030))
    month_range = list(range(1, 13))
    day_range = list(range(1, 32))
    context = {
        'year_range': year_range,
        'month_range': month_range,
        'day_range': day_range,
        'classes': EM2_classes,
    }
    date_class_html = loader.get_template("home/date_class.html")
    return HttpResponse(date_class_html.render(context, request))

def dateclass_redirect(request):
    try:
        year = request.POST["year"]
        month = request.POST["month"]
        day = request.POST["day"]
        class_num = request.POST["class"]
    except:
        pass
    date = year + month + day
    return redirect('/classreport/date=%s/class=%s' % (str(date), str(class_num)))

def classreport(request, date, class_num):
    return HttpResponse('Hello, world!')
    """
    classstat_html = loader.get_template('home/classstat.html')
    context = {
        'class_num': class_num,
    }
    return HttpResponse(classstat_html.render(context, request))
    """

def roster_upload(request):
    # show the list of courses
    ################################################################
    """
    courses = Course.objects.all().order_by("-year", "semester", "course_name", "class_num")
    course_cnt = courses.count()
    courses_dict = OrderedDict()
    for course in courses:
        course_title = str(course.year)+'-'+str(course.semester)+' '+course.course_name + " - Class " + str(course.class_num)
        course_token = course.course_token
        courses_dict[course_token] = course_title
        """
    course = Course.find_active_course()
    course_title = str(course.year)+'-'+str(course.semester)+' '+course.course_name + " - Class " + str(course.class_num)
    roster_upload_html = loader.get_template("home/roster_upload.html")
    context = {
        "course_title": course_title,
    }
    return HttpResponse(roster_upload_html.render(context, request))

def excel_upload_handler(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if request.method == "POST" and request.FILES['excel']:
        excel = request.FILES['excel']
        with open(BASE_DIR+'/data/temp/rosterupload/'+excel.name, 'wb+') as io:
            io.write(excel.read())
        return redirect('/faculty/sysstat/classinit/%s/preview/' % excel.name)

def excelpreview(request, filename):
    roster, student_cnt = excel_read(file_name=filename)
    context = {
        'filename': filename,
        'affiliation': np.ndarray.tolist(roster[:,0]),
        'major': np.ndarray.tolist(roster[:,1]),
        'grade': np.ndarray.tolist(roster[:,2]),
        'id_num': np.ndarray.tolist(roster[:,3]),
        'eng_name': np.ndarray.tolist(roster[:,4]),
        'kor_name': np.ndarray.tolist(roster[:,5]),
        'email': np.ndarray.tolist(roster[:,6]),
        'student_cnt': student_cnt,
        'students': list(range(0, student_cnt)),
    }
    excelpreview_html = loader.get_template("home/excel_preview.html")
    return HttpResponse(excelpreview_html.render(context, request))

def register_students_handler(request, file_name):
    data, student_cnt = excel_read(file_name=file_name)
    course = Course.objects.get(is_active=True)

    for idx in range(student_cnt):
        user = User.objects.create_user(username=str(data[idx,3]),
        password=str(data[idx,3]),
        email=data[idx,6],
        first_name=data[idx,4])

        student = Student.objects.create(user=user, id_text=data[idx,3],
        name_text_korean=data[idx,5],
        name_text_english=data[idx,4],
        class_num=course.class_num,
        major_text=data[idx,1],
        grade=data[idx,2])
        student.enrolled_course.add(course)
        student.save()
    return redirect("home:register_result")

def student_registration_result(request):
    course = Course.objects.get(is_active=True)
    student_cnt = course.student_set.all().count()
    course_title = str(course.year)+'-'+str(course.semester)+' '+course.course_name + " - Class " + str(course.class_num)
    context = {
        "course_title": course_title,
        "student_cnt": student_cnt,
    }
    reg_result_html = loader.get_template("home/register_result.html")
    return HttpResponse(reg_result_html.render(context, request))

def select_course(request):
    # deactivate the system before course selection
    ################################################################
    try:
        Course.find_active_course(deactivate=True)
    except Course.DoesNotExist:
        pass

    # show the list of courses
    ################################################################
    courses = Course.objects.all().order_by("-year", "semester", "course_name", "class_num")
    course_cnt = courses.count()
    courses_dict = OrderedDict()
    for course in courses:
        course_title = str(course.year)+'-'+str(course.semester)+' '+course.course_name + " - Class " + str(course.class_num)
        course_token = course.course_token
        courses_dict[course_token] = course_title

    # parse context and html template to the client
    select_course_html = loader.get_template('home/instructor_select_course.html')
    context = {
        "courses_dict": courses_dict.items(),
        "courses": range(course_cnt),
    }
    return HttpResponse(select_course_html.render(context, request))

def course_selection_handler(request):
    Course.close_all()
    course_token = request.POST["course_token"]
    course = Course.objects.get(course_token=course_token)
    course.is_active = True
    course.save()
    return redirect("home:faculty")

def student_change_password(request):
    context = {}
    student_change_password_handler = loader.get_template("home/change_password.html")
    return HttpResponse(student_change_password_handler.render(context, request))

def student_password_handler(request):
    current_user = request.user
    cpwd, npwd = request.POST["cpwd"], request.POST["npwd"]

    if authenticate(username=current_user.username, password=cpwd) is not None:
        current_user.set_password(npwd)
        current_user.save()
        return redirect("home:student_password_success")
    else:
        return redirect("home:student_password_error")

def student_password_error(request):
    student_password_error_html = loader.get_template("registration/change_password_error.html")
    context = {}
    return HttpResponse(student_password_error_html.render(context, request))

def student_password_success(request):
    student_password_success_html = loader.get_template("registration/change_password_success.html")
    context = {}
    return HttpResponse(student_password_success_html.render(context, request))

def excel_read(file_name, return_base_dir=False):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    roster = pandas.read_excel(BASE_DIR+'/data/temp/rosterupload/'+file_name, sheet_name=0).as_matrix()
    student_cnt = roster.shape[0]
    if return_base_dir:
        return roster, student_cnt, BASE_DIR
    else:
        return roster, student_cnt

def student_calibration(request):
    student_calibration_html = loader.get_template("home/student_calibration.html")
    context = {}
    return HttpResponse(student_calibration_html.render(context, request))

def student_calibration_handler(request):
    course = Course.find_active_course()
    username = request.user.username
    password = request.POST["password"]
    if authenticate(username=username, password=password) is not None:
        course.student_set.all().delete()
        return redirect("home:calibration_result")
    else:
        return redirect("home:student_calibration")



def calibration_result(request):
    calibration_result_html = loader.get_template("home/calibration_result.html")
    context = {}
    return HttpResponse(calibration_result_html.render(context, request))
