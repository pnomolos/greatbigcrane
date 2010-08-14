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

import tempfile

from buildout_manage import recipes
from buildout_manage.buildout_config import BuildoutConfig, buildout_parse, buildout_write

"""
Notes:
* Add a djangorecipe section to a BuildoutConfig
"""

class RecipeTests(TestCase):
    def test_add_djangorecipe_to_buildoutconfig(self):
        bc = BuildoutConfig()
        djangorecipe = recipes['djangorecipe']

        dr = djangorecipe(bc, 'django')

        dr.settings = 'development'
        dr.version = '1.2.1'
        dr.eggs = ('eggs', 'eggs')
        dr.project = 'greatbigcrane'
        dr.extra_paths = ('eggs', 'extra-paths')
        dr.fcgi = True
        dr.wsgi = False

        django = bc['django']
        assert django

        assert django['recipe'] == 'djangorecipe'
        assert django['settings'] == 'development'
        assert django['version'] == '1.2.1'
        assert django['eggs'] == '${eggs:eggs}'
        assert django['project'] == 'greatbigcrane'
        assert django['extra-paths'] == '${eggs:extra-paths}'
        assert django['fcgi'] == 'True'
        assert django['wsgi'] == 'False'

        fp = tempfile.NamedTemporaryFile()

        buildout_write(fp.name, bc)

        data = fp.read()
        assert data == """[buildout]
parts = 
\tdjango

[django]
recipe = djangorecipe
settings = development
version = 1.2.1
eggs = ${eggs:eggs}
project = greatbigcrane
extra-paths = ${eggs:extra-paths}
fcgi = True
wsgi = False

"""

from buildout_config_tests import *
