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
from buildout_manage.recipetools import simple_property, bool_property

class GitRecipe(object):
    def __init__(self, config, section_name):
        self.config = config
        self.section_name = section_name

    def init(self):
        # Does section already exist?
        self.config.add_part(self.section_name)
        self.section = self.config[self.section_name]
        self.section['recipe'] = 'zerokspot.recipe.git'

    def dict(self):
        return dict(repository=self.repository,
                rev=self.rev,
                branch=self.branch,
                paths=self.paths,
                newest=self.newest,
                as_egg=self.as_egg,
                cache_name=self.cache_name)

    repository = simple_property('repository')
    rev = simple_property('rev')
    branch = simple_property('branch')
    paths = simple_property('paths')
    newest = bool_property('newest')
    as_egg = bool_property('as_egg')
    cache_name = simple_property('cache-name')

def git(config, section_name):
    recipe = GitRecipe(config, section_name)
    recipe.init()
    return recipe

