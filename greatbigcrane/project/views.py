from django.shortcuts import render_to_response
from django.views.generic.list_detail import object_list
from project.models import Project

def index(request):
    '''We should move this to a different app'''
    return render_to_response('index.html')

def list_projects(request):
    projects = Project.objects.all()
    return object_list(request, projects, template_name="project/project_list.html",
            template_object_name="project")

def view_project(request, project_id):
    from django.http import HttpResponse
    return HttpResponse("not implemented")
