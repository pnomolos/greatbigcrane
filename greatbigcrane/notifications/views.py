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

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic.list_detail import object_list
from django.http import HttpResponse
from notifications.models import Notification

def list_notifications(request):
    notifications = Notification.objects.all()
    return object_list(request, notifications,
            template_name="notifications/notification_list.html",
            template_object_name="notification", paginate_by=10)

def view_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    return render_to_response("notifications/notification.html",
            RequestContext(request, {'notification': notification}))

def dismiss_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.dismissed = True
    notification.save()
    return HttpResponse("success")
