from django.shortcuts import render_to_response
from django.views.generic.list_detail import object_list
from django.views.generic.list_detail import object_detail
from django.views.generic.create_update import create_object
from project.models import Project

def index(request):
    '''We should move this to a different app'''
    return render_to_response('index.html')

def list_projects(request):
    projects = Project.objects.all()
    return object_list(request, projects, template_name="project/project_list.html",
            template_object_name="project")

def view_project(request, project_id):
    return object_detail(request, Project.objects.all(), object_id=project_id,
            template_object_name='project')

def add_project(request):
    # We have to do stuff like create the buildout directory on save
    # so this can't stay generic
    return create_object(request, model=Project)
