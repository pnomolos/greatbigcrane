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

urlpatterns = patterns('job_queue.views',
        url('^(?P<project_id>\d+)/buildout/$', 'schedule_buildout', name="schedule_buildout"),
        url('^(?P<project_id>\d+)/bootstrap/$', 'schedule_bootstrap', name="schedule_bootstrap"),
        url('^(?P<project_id>\d+)/test/$', 'schedule_test', name="schedule_test"),
        url('^(?P<project_id>\d+)/pull/$', 'schedule_pull', name="schedule_pull"),
        url('^(?P<project_id>\d+)/syncdb/$', 'schedule_syncdb', name="schedule_syncdb"),
        url('^(?P<project_id>\d+)/startapp/$', 'startapp', name="startapp"),
        url('^(?P<project_id>\d+)/migrate/$', 'schedule_migrate', name="schedule_migrate"),
        url('^(?P<project_id>\d+)/edit_buildout/$', 'edit_buildout', name="edit_buildout"),
        url('^(?P<project_id>\d+)/virtualenv/$', 'schedule_virtualenv', name="schedule_virtualenv"),
        )
