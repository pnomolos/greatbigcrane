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

class MercurialRecipe(object):
    def __init__(self, config, section_name):
        self.config = config
        self.section_name = section_name

    def init(self):
        # Does section already exist?
        add_parts(self.config, self.section_name)
        self.section = self.config[self.section_name]
        self.section['recipe'] = 'mercurialrecipe'

    def dict(self):
        return dict(repository=self.repository,
                location=self.location,
                newest=self.newest)

    repository = simple_property('repository')
    location = simple_property('location')
    newest = bool_property('newest')

def mercurial(config, section_name):
    recipe = MercurialRecipe(config, section_name)
    recipe.init()
    return recipe

