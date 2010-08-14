from django.conf.urls.defaults import *

urlpatterns = patterns('project.views',
        url('^$', 'list_projects', name="list_projects"),
        url('^view/(?P<project_id>\d+)/$', 'view_project', name="view_project"),
        )
