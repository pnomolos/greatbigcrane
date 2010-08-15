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
import json
from shutil import copyfile

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic.list_detail import object_list
from django.views.generic.list_detail import object_detail
from django.views.generic.create_update import delete_object
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.forms.util import ErrorList

import buildout_manage
from job_queue.jobs import queue_job
from project.models import Project
from project.forms import ProjectForm, recipe_form_map
from preferences.models import Preference
from notifications.models import Notification

def index(request):
    '''We should move this to a different app. Possibly preferences, it's more generic.'''
    projects = Project.objects.filter(favourite=False).order_by('-updated_at')[:5]
    favourite_projects = Project.objects.filter(favourite=True).order_by('name')
    notifications = Notification.objects.exclude(dismissed=True)[:10]
    return render_to_response('index.html', RequestContext(request,
        {'project_list': projects, 'favourite_project_list': favourite_projects, 'notifications': notifications}))

def about(request):
    '''Also go to another app or flatpage...'''
    return render_to_response('about.html', RequestContext(request))

def list_projects(request):
    orderby = request.GET.get('orderby', 'name')
    projects = Project.objects.all().order_by(orderby)
    return object_list(request, projects, template_name="project/project_list.html",
            template_object_name="project", extra_context={'orderby': orderby})

def view_project(request, project_id):
    return object_detail(request, Project.objects.all(), object_id=project_id,
            template_object_name='project')

def add_project(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        try:
            base_dir = form.cleaned_data['base_directory']
            
            if form.cleaned_data['git_repo']:
                target_dir = os.path.dirname(base_dir)
            else:
                target_dir = base_dir
            if not os.path.isdir(target_dir):
                os.makedirs(target_dir)
                
            if form.cleaned_data['git_repo']:
                instance = form.save()
                queue_job("GITCLONE", project_id=instance.id)
            else:
                skeleton = [(os.path.join(settings.PROJECT_HOME, "../bootstrap.py"),
                        os.path.join(target_dir, "bootstrap.py")),
                    (os.path.join(settings.PROJECT_HOME, "../base_buildout.cfg"),
                        os.path.join(target_dir, "buildout.cfg"))]
                for source, dest in skeleton:
                    if not os.path.isfile(dest):
                        copyfile(source, dest)
                instance = form.save()
                queue_job("BOOTSTRAP", project_id=instance.id)
                
            return redirect(instance.get_absolute_url())
            
        except IOError as e:
            errors = form._errors.setdefault("base_directory", ErrorList())
            errors.append(u"An error occurred: " + str(e))

    base_url = Preference.objects.get_preference("projects_directory", '')

    return render_to_response("project/project_form.html",
            RequestContext(request, {'form': form, 'base_url': base_url}))

def delete_project(request, project_id):
    return delete_object(request, model=Project, object_id=project_id,
            post_delete_redirect=reverse("list_projects"))

def favourite_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    project.favourite=not project.favourite
    project.save()
    return handle_ajax(request)

def add_recipe(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render_to_response("project/add_recipe.html", 
            RequestContext(request, {
                'project': project,
                'available_recipes': buildout_manage.recipes}))

def edit_recipe(request, project_id, recipe_name):
    #FIXME: rename recipe_name to section_name to avoid confusion
    # and recipe_type to recipe_name
    project = get_object_or_404(Project, id=project_id)
    buildout=project.buildout()
    section=buildout[recipe_name]
    recipe_type = section['recipe']
    recipe = buildout_manage.recipes[recipe_type](buildout, recipe_name)

    form = recipe_form_map[recipe_type](project, initial=recipe.dict())
    return render_to_response("project/edit_recipe.html", RequestContext(
        request, {'form': form,
            'template_name': "project/recipe_templates/%s.html" % recipe_type,
            'recipe_name': recipe_type,
            'project': project}))

def recipe_template(request, project_id, recipe_name):
    project = get_object_or_404(Project, id=project_id)
    form = recipe_form_map[recipe_name](project)
    return render_to_response("project/recipe_templates/%s.html" % recipe_name,
            {'form': form})

@require_POST
def save_recipe(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    recipe_name = request.POST['recipe_name']
    form = recipe_form_map[recipe_name](project, request.POST)
    if form.is_valid():
        buildout = project.buildout()
        form.save(buildout)
        return redirect(project.get_absolute_url())
    else:
        return render_to_response("project/recipe_templates/%s.html" % recipe_name,
                {'form': form})


def handle_ajax(request):
    # return HttpResponse(request.POST['update'])
    if 'update' in request.POST:
        update = dict()
        d = json.loads(request.POST['update'])
        for k,v in d.items():
            if v == 'projects':
                update[k] = Project.objects.all().order_by(request.GET.get('orderby', 'name'))
            elif v == 'home-projects':
                update[k] = Project.objects.filter(favourite=False).order_by('-updated_at')[:5]
            elif v == 'favourite-projects':
                update[k] = Project.objects.filter(favourite=True).order_by('name')
            
            update[k] = render_to_string("project/_project_list.html", RequestContext(request,
                    {'project_list': update[k]}))
        
        return HttpResponse(json.dumps({'update': update}),content_type="application/json")
    else:
        return HttpResponse('fail')

def schedule_buildout(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    try:
        queue_job("BUILDOUT", project_id=project.id)
        return HttpResponse('Successfully queued buildout')
    except Exception as e:
        return HttpResponseServerError("Error: " + str(e))

def schedule_test(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    try:
        queue_job("TEST", project_id=project.id)
        return HttpResponse('Successfully queued test')
    except Exception as e:
        return HttpResponseServerError("Error: " + str(e))

def schedule_pull(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    try:
        queue_job("GITPULL", project_id=project.id)
        return HttpResponse('Successfully queued git pull')
    except Exception as e:
        return HttpResponseServerError("Error: " + str(e))
