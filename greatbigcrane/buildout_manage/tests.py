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

from buildout_config_tests import *

"""
Notes:
* *Add a djangorecipe section to a BuildoutConfig*
* *Parse an existing djangorecipe section*
* *Parse an existing djangorecipe section, modify it, and write it out again*
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

    def test_parse_djangorecipe(self):
        fp = mktmpcfg(complicated_buildout_cfg)
        bc = buildout_parse(fp.name)

        djangorecipe = recipes['djangorecipe']
        dr = djangorecipe(bc, 'django')

        assert dr.settings == 'development'
        assert dr.version == '1.2.1'
        assert dr.extra_paths == ('eggs', 'extra-paths')
        assert dr.fcgi == True

    def test_change_existing_djangorecipe(self):
        fp = mktmpcfg(complicated_buildout_cfg)
        bc = buildout_parse(fp.name)

        djangorecipe = recipes['djangorecipe']
        dr = djangorecipe(bc, 'django')

        dr.settings = 'production'
        dr.version = '1.1.1'
        dr.fcgi = False
        dr.wsgi = False
        dr.eggs = [dr.eggs, ('pyzmq', 'parts')]

        fp.seek(0)
        buildout_write(fp.name, bc)
        
        data = fp.read()
        assert data == """[buildout]
parts = 
\teggs
\tdjango
\tpyzmq
unzip = true

[eggs]
recipe = zc.recipe.egg
eggs = 
\tsouth==0.7.1
\tIPython
extra-paths = 
\t${buildout:directory}/parts/django
\t${buildout:directory}/parts/django-registration
\t${buildout:directory}/greatbigcrane
\t${buildout:directory}/parts/pyzmq

[django]
settings = production
recipe = djangorecipe
version = 1.1.1
eggs = 
\t${eggs:eggs}
\t${pyzmq:parts}
project = greatbigcrane
extra-paths = ${eggs:extra-paths}
fcgi = False
wsgi = False

[pyzmq]
recipe = zerokspot.recipe.git
repository = http://github.com/zeromq/pyzmq.git
as_egg = True

"""
