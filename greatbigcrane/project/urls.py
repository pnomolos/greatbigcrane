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

from django.conf.urls.defaults import *

urlpatterns = patterns('project.views',
        url('^$', 'list_projects', name="list_projects"),
        url('^(?P<project_id>\d+)/view/$', 'view_project', name="view_project"),
        url('^(?P<project_id>\d+)/buildout/$', 'schedule_buildout', name="schedule_buildout"),
        url('^(?P<project_id>\d+)/test/$', 'schedule_test', name="schedule_test"),
        url('^(?P<project_id>\d+)/pull/$', 'schedule_pull', name="schedule_pull"),
        url('^add/$', 'add_project', name="add_project"),
        url('^(?P<project_id>\d+)/favourite/$', 'favourite_project', name="favourite_project"),
        url('^(?P<project_id>\d+)/add_recipe/$', 'add_recipe', name="add_recipe"),
        url('^(?P<project_id>\d+)/recipe/(?P<recipe_name>[^/]*)/edit/$', 'edit_recipe', name="edit_recipe"),
        url('^(?P<project_id>\d+)/save_recipe/$', 'save_recipe', name="save_recipe"),
        url('^(?P<project_id>\d+)/recipe_template/(?P<recipe_name>[^/]*)/$', 'recipe_template', name='recipe_template')
        )
