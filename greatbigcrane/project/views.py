"""
Copyright 2010 Jason Chu, Dusty Phillips, and Phil Schalm

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os.path
from shutil import copyfile

from django.shortcuts import render_to_response, redirect
from django.views.generic.list_detail import object_list
from django.views.generic.list_detail import object_detail
from django.template import RequestContext
from django.conf import settings

from job_queue.jobs import queue_job
from project.models import Project
from project.forms import ProjectForm
from preferences.models import Preference
from notifications.models import Notification

def index(request):
    '''We should move this to a different app. Possibly preferences, it's more generic.'''
    projects = Project.objects.all()
    notifications = Notification.objects.all()[:10]
    print notifications
    return render_to_response('index.html', RequestContext(request,
        {'project_list': projects, 'notifications': notifications}))

def list_projects(request):
    projects = Project.objects.all()
    if "orderby" in request.GET:
        projects = projects.order_by(request.GET['orderby'])
    return object_list(request, projects, template_name="project/project_list.html",
            template_object_name="project")

def view_project(request, project_id):
    return object_detail(request, Project.objects.all(), object_id=project_id,
            template_object_name='project')

def add_project(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        os.makedirs(instance.base_directory)
        copyfile(os.path.join(settings.PROJECT_HOME, "../bootstrap.py"),
                os.path.join(instance.base_directory, "bootstrap.py"))
        queue_job("BOOTSTRAP", project_id=instance.id)
        return redirect(instance.get_absolute_url())

    base_url = Preference.objects.get_preference("projects_directory", '')

    return render_to_response("project/project_form.html",
            RequestContext(request, {'form': form, 'base_url': base_url}))
