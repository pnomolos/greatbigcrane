from django.conf.urls.defaults import *

urlpatterns = patterns('preferences.views',
        url('^$', 'preferences', name="preferences"),
)
