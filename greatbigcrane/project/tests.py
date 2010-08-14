from django.test import TestCase
from django.template import Template, RequestContext

class MockPathRequest(object):
    def __init__(self, path):
        self.path = path

class HelperTest(TestCase):
    '''tests for the helper template tags'''

    def test_nav_url_tag_matches_root(self):
        template = Template("{% load helpers %}<a {% nav_url '/' %}>")
        request = MockPathRequest("/")
        context = RequestContext(request, {})
        rendered = template.render(context)
        assert rendered == '<a href="/" class="current">'

    def test_nav_url_not_root_current(self):
        template = Template("{% load helpers %}<a {% nav_url '/projects/' %}>")
        request = MockPathRequest("/")
        context = RequestContext(request, {})
        rendered = template.render(context)
        assert rendered == '<a href="/projects/">'

    def test_nav_url_not_current_root(self):
        template = Template("{% load helpers %}<a {% nav_url '/' %}>")
        request = MockPathRequest("/projects/")
        context = RequestContext(request, {})
        rendered = template.render(context)
        assert rendered == '<a href="/">'

    def test_nav_url_full_path(self):
        template = Template("{% load helpers %}<a {% nav_url '/projects/' %}>")
        request = MockPathRequest("/projects/")
        context = RequestContext(request, {})
        rendered = template.render(context)
        assert rendered == '<a href="/projects/" class="current">'
