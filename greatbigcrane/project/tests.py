from django.test import TestCase
from django.template import Template, RequestContext

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

from buildout_config_tests import *
