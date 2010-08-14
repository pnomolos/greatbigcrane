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

from buildout_manage import recipetools

def simple_property_get(name):
    def get(self):
        # FIXME: Parse ${
        return self.section[name]
    return get

def simple_property_set(name):
    def set(self, value):
        def convert_value(data):
            if isinstance(data, tuple):
                data = '${%s:%s}' % data
            return data

        if isinstance(value, list):
            value = [convert_value(x) for x in value]
        else:
            value = convert_value(value)
        self.section[name] = value
    return set

def simple_property_delete(name):
    def delete(self):
        del self.section[name]
    return delete

simple_property = lambda name: property(simple_property_get(name), simple_property_set(name), simple_property_delete(name))

def bool_property_get(name):
    def get(self):
        value = self.section[name]
        if value.lower() == 'true':
            return True
        return False
    return get

def bool_property_set(name):
    def set(self, value):
        if value == True:
            value = 'True'
        else:
            value = 'False'
        self.section[name] = value
    return set

bool_property = lambda name: property(bool_property_get(name), bool_property_set(name), simple_property_delete(name))

class DjangoRecipe(object):
    def __init__(self, config, section_name):
        self.config = config
        self.section_name = section_name

    def init(self):
        # Does section already exist?
        recipetools.add_parts(self.config, self.section_name)
        self.section = self.config[self.section_name]
        self.section['recipe'] = 'djangorecipe'

    settings = simple_property('settings')
    version = simple_property('version')
    eggs = simple_property('eggs')
    project = simple_property('project')
    extra_paths = simple_property('extra-paths')
    fcgi = bool_property('fcgi')
    wsgi = bool_property('wsgi')

def django(config, section_name):
    recipe = DjangoRecipe(config, section_name)
    recipe.init()
    return recipe
