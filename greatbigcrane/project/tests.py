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

from django.test import TestCase
from django.template import Template, RequestContext
from project.models import Project

class MockPathRequest(object):
    def __init__(self, path):
        self.path = path

class HelperTest(TestCase):
    '''tests for the helper template tags'''

    def nav_url_test(self, template_string, request_path, expected):
        template = Template(template_string)
        request = MockPathRequest(request_path)
        context = RequestContext(request, {})
        rendered = template.render(context)
        assert rendered == expected

    def test_nav_url_tag_matches_root(self):
        return self.nav_url_test("{% load helpers %}<a {% nav_url '/' %}>", "/",
                '<a href="/" class="current">')

    def test_nav_url_not_root_current(self):
        return self.nav_url_test(
                "{% load helpers %}<a {% nav_url '/projects/' %}>", "/",
                '<a href="/projects/">')

    def test_nav_url_not_current_root(self):
        return self.nav_url_test("{% load helpers %}<a {% nav_url '/' %}>",
                '/projects/', '<a href="/">')

    def test_nav_url_full_path(self):
        return self.nav_url_test(
                "{% load helpers %}<a {% nav_url '/projects/' %}>",
                '/projects/', '<a href="/projects/" class="current">')

    def test_nav_url_partial_path(self):
        return self.nav_url_test(
                "{% load helpers %}<a {% nav_url '/projects/' %}>",
                "/projects/cool/",
                '<a href="/projects/" class="current">')

    def test_nav_url_sub_path(self):
        return self.nav_url_test(
                "{% load helpers %}<a {% nav_url '/projects/cool/' '/projects/' %}>",
                "/projects/food/",
                '<a href="/projects/cool/" class="current">')

class ProjectGithubUrlTests(TestCase):
    def test_ssh_url(self):
        p = Project(name="great big crane",
                git_repo="git@github.com:pnomolos/Django-Dash-2010.git")
        assert p.github_url() == "http://github.com/pnomolos/Django-Dash-2010"

    def test_http_url(self):
        p = Project(name="great big crane", 
                git_repo="https://buchuki@github.com/pnomolos/Django-Dash-2010.git")
        assert p.github_url() == "http://github.com/pnomolos/Django-Dash-2010"

    def test_git_readonly_url(self):
        p = Project(name="great big crane", 
                git_repo="git://github.com/pnomolos/Django-Dash-2010.git")
        assert p.github_url() == "http://github.com/pnomolos/Django-Dash-2010"

    def test_no_git(self):
        p = Project(name="great big crane", 
                git_repo="git://github.com/pnomolos/Django-Dash-2010")
        assert p.github_url() == "http://github.com/pnomolos/Django-Dash-2010"
