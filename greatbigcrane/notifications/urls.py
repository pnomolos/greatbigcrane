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

urlpatterns = patterns('notifications.views',
        url('^$', 'list_notifications', name="list_notifications"),
        url('^ajax$', 'ajax_notification', name="ajax_notification"),
        url('^dismiss/(?P<notification_id>\d+)/$', 'dismiss_notification',
            name='dismiss_notification'),
        url('^view/(?P<notification_id>\d+)/$', 'view_notification', name="view_notification"),
        )
