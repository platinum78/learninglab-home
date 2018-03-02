from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader

# Create your views here.
def index(request):
    # return HttpResponse("Welcome! You're in the roster index page.")
    html = loader.get_template('roster/index.html')
    return HttpResponse(html.render())

def set_groups(request):
    groups_html = loader.get_template("roster/set_groups.html")
    context = {}
    return HttpResponse(groups_html.render(context, request))
