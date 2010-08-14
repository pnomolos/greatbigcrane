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
        url('^view/(?P<project_id>\d+)/$', 'view_project', name="view_project"),
        url('^add/$', 'add_project', name="add_project"),
        url('^favourite/(?P<project_id>\d+)/$', 'favourite_project', name="favourite_project"),
        url('^add_recipe/(?P<project_id>\d+)/$', 'add_recipe', name="add_recipe")
        )
