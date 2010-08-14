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
from django.db import models
from django.core.urlresolvers import reverse
from buildout_manage.buildout_config import buildout_parse


class Project(models.Model):
    name = models.CharField(max_length=32)
    base_directory = models.CharField(max_length=512, unique=True)
    git_repo = models.CharField(max_length=512, blank=True, default='')
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    test_status = models.BooleanField(default=False)
    favourite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("view_project", args=[self.id])

    def buildout_sections(self):
        '''Return sorted dictionary of buildout sections'''
        buildout_filename = os.path.join(self.base_directory, 'buildout.cfg')
        sections = buildout_parse(buildout_filename)
        return sections
        
    def __unicode__(self):
        return self.name
