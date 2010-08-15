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

from buildout_manage.recipetools import add_parts, simple_property, bool_property

class DjangoRecipe(object):
    def __init__(self, config, section_name):
        self.config = config
        self.section_name = section_name

    def init(self):
        # Does section already exist?
        add_parts(self.config, self.section_name)
        self.section = self.config[self.section_name]
        self.section['recipe'] = 'djangorecipe'

    def dict(self):
        return dict(settings=self.settings,
                version=self.version,
                eggs=self.eggs,
                project=self.project,
                extra_paths=self.extra_paths,
                fcgi=self.fcgi,
                wsgi=self.wsgi)

    settings = simple_property('settings')
    version = simple_property('version')
    eggs = simple_property('eggs')
    project = simple_property('project')
    extra_paths = simple_property('extra-paths')
    fcgi = bool_property('fcgi')
    wsgi = bool_property('wsgi')
    test = simple_property('test')

def django(config, section_name):
    recipe = DjangoRecipe(config, section_name)
    recipe.init()
    return recipe
