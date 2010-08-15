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
from buildout_manage.parser import buildout_parse


class Project(models.Model):
    name = models.CharField(max_length=32)
    base_directory = models.CharField(max_length=512, unique=True)
    git_repo = models.CharField(max_length=512, blank=True, default='')
    description = models.TextField(blank=True, help_text="(Markdown syntax is supported)")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    test_status = models.BooleanField(default=False)
    favourite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("view_project", args=[self.id])

    def buildout_sections(self):
        '''Return sorted dictionary of buildout sections'''
        sections = self.buildout()
        # You may wonder why I'm returning items. I am too. For unknown
        # reasons, {{project.buildout_sections.items}} does not return a
        # correct value inside templates.
        return sections.items()

    def buildout_filename(self):
        return os.path.join(self.base_directory, 'buildout.cfg')

    def buildout(self):
        sections = buildout_parse(self.buildout_filename())
        return sections

    def is_django(self):
        sections = self.buildout()
        for name, section in sections.items():
            if 'recipe' in section and section['recipe'] == 'djangorecipe':
                return True
        return False

    def github_url(self):
        '''If our repo is a github repo, provide a link to the
        github page.'''
        github = self.git_repo.find("github.com")
        if github > -1:
            url = self.git_repo[github:].replace(":", "/")
            if url.endswith(".git"):
                url = url[:-4]
            url = "http://%s" % url
        else:
            url = ""
        return url

    def __unicode__(self):
        return self.name
