from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import Context, loader

from roster.models import *
from courses.models import *

# Create your views here.
def index(request):
    # return HttpResponse("Welcome! You're in the roster index page.")
    course = Course.objects.get(is_active=True)
    full_roster = Student.objects.filter(enrolled_course=course)
    index_html = loader.get_template('roster/index.html')
    context = {
        "full_roster": full_roster,
    }
    return HttpResponse(index_html.render(context, request))

def set_groups(request):
    groups_html = loader.get_template("roster/set_groups.html")
    context = {}
    return HttpResponse(groups_html.render(context, request))

def grouping_manual(request):
    grouping_manual_html = loader.get_template("roster/grouping_manual.html")
    course = Course.objects.get(is_active=True)

    full_roster = Student.objects.filter(enrolled_course=course)
    names = []
    student_numbers = []
    for student in full_roster:
        names.append(student.name_text_korean)
        student_numbers.append(student.id_text)

    context = {
        # "names": names,
        # "student_numbers": student_numbers,
        # "students": list(range(len(full_roster))),
        "course_title": course.title(),
        "full_roster": full_roster,
    }
    return HttpResponse(grouping_manual_html.render(context, request))

def grouping_excel(request):
    course = Course.objects.get(is_active=True)
    grouping_excel_html = loader.get_template("roster/roster_upload.html")
    context = {
        'course_title': course.title(),
    }
    return HttpResponse(grouping_excel_html.render(context, request))

def grouping_excelupload_handler(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if request.method == "POST" and request.FILES['excel']:
        excel = request.FILES['excel']
        with open(BASE_DIR+'/data/temp/rosterupload/'+excel.name, 'wb+') as io:
            io.write(excel.read())
            return redirect('/roster/groups/roster/%s/preview/' % excel.name)

def grouping_handler_excel(request, filename):
    roster, student_cnt = excel_read(file_name=filename)
    missing = 0
    for idx in roster.shape[0]:
        try:
            id_num = roster[idx,0]
            group_num = roster[idx, 4]
            student = Student.objects.get(id_text=id_num)
            student.group_num = group_num
            student.save()
        except Student.DoesNotExist:
            missing += 1
            pass
    return redirect("roster:grouping_result")

def grouping_result(request):
    pass

def grouping_excel_preview(request, file_name):
    roster, student_cnt = excel_read(file_name=filename)
    context = {
        'filename': filename,
        'icampus_id': np.ndarray.tolist(roster[:,3]),
        'id_num': np.ndarray.tolist(roster[:,4]),
        'kor_name': np.ndarray.tolist(roster[:,6]),
        'student_cnt': student_cnt,
        'students': list(range(0, student_cnt)),
    }
    excelpreview_html = loader.get_template("home/excel_preview.html")
    return HttpResponse(excelpreview_html.render(context, request))

def grouping_handler(request):
    for student in Student.objects.all():
        student.group_num = request.POST[student.id_text]
        student.save()
    return HttpResponse("Group addition finished!")


def group_batch_assignment(requst):
    pass

def excel_read(file_name, return_base_dir=False):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    roster = pandas.read_excel(BASE_DIR+'/data/temp/rosterupload/'+file_name, sheet_name=0).as_matrix()
    student_cnt = roster.shape[0]
    if return_base_dir:
        return roster, student_cnt, BASE_DIR
    else:
        return roster, student_cnt
