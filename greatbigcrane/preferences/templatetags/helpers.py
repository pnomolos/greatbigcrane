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

from django import template

register = template.Library()

# Based on http://stackoverflow.com/questions/340888/navigation-in-django/1800535#1800535
@register.tag
def nav_url(parser, token):
    '''{% active url %} maps to href="url" and also adds class="url" only if
    the current page is the given url. {% active url current %} maps to
    href="url" and also adds class="url" if the curent page starts with the
    current url.'''
    args = token.split_contents()
    template_tag = args[0]
    if len(args) < 2 or len(args) > 3:
        raise template.TemplateSyntaxError, "%r tag requires the url to link to, and an optional path to compare with" % template_tag
    return NavSelectedNode(*args[1:])

class NavSelectedNode(template.Node):
    def __init__(self, url, current=None):
        self.url = url
        self.current = current if current else url

    def render(self, context):
        current_path = context['request'].path
        expected_path = template.Variable(self.current).resolve(context)
        url = template.Variable(self.url).resolve(context)
        if expected_path in ('/', '') and not current_path in ('/', ''):
            selected = ""
        elif current_path.startswith(expected_path):
            selected = ' class="current"'
        else:
            selected = ""
        return 'href="%s"%s' % (url, selected) 

