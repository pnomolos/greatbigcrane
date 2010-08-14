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

import tempfile

from greatbigcrane.buildout_manage.buildout_config import buildout_parse, BuildoutConfig, buildout_write

"""
Notes:
* *Parse simplest buildout.cfg*
* *Parse more complicated buildout.cfg*

* *Write simplest buildout.cfg*
* *Write more complicated buildout.cfg*
* *Write config and make sure sections order is preserved*
* *Write config and make sure lists of things are separated by newlines and indents properly*
"""

class BuildoutParse(TestCase):
    """Tests for buildout_parse module"""

    def test_parse_simplest_buildout(self):
        fp = mktmpcfg(simple_buildout_cfg)
        buildout_object = buildout_parse(fp.name)

        assert buildout_object['buildout']['parts'] == ''

    def test_parse_complicated_buildout(self):
        fp = mktmpcfg(complicated_buildout_cfg)
        buildout_object = buildout_parse(fp.name)

        assert buildout_object['buildout'].keys() == ['parts', 'unzip']

        assert buildout_object['buildout']['parts'] == ['eggs', 'django', 'pyzmq']

    def test_write_simplest_buildout(self):
        bc = BuildoutConfig()
        bc['buildout']['parts'] = ''
        bc['buildout']['find-links'] = 'http://pypi.python.org/simple'

        fp = tempfile.NamedTemporaryFile()

        buildout_write(fp.name, bc)

        data = fp.read()
        assert data == '''[buildout]
parts = 
find-links = http://pypi.python.org/simple

'''

    def test_write_simplest_list_buildout(self):
        bc = BuildoutConfig()
        bc['buildout']['parts'] = ''
        bc['buildout']['find-links'] = ['http://pypi.python.org/simple', 'http://python.org']

        fp = tempfile.NamedTemporaryFile()

        buildout_write(fp.name, bc)

        data = fp.read()
        assert data == '''[buildout]
parts = 
find-links = 
\thttp://pypi.python.org/simple
\thttp://python.org

'''

    def test_write_obscene_amount_of_sections(self):
        bc = BuildoutConfig()

        bc['buildout']['parts'] = ''
        bc['1section']['a'] = '1'
        bc['8section']['b'] = '3'
        bc['2section']['c'] = '4'
        bc['something']['d'] = '99eleven'
        bc['09876']['d'] = ['yes', 'again']
        bc['dusty']['kkkkk'] = ''
        bc['dusty']['kkkk'] = ''
        bc['dusty']['k'] = ''
        bc['dusty']['kk'] = ''
        bc['dusty']['kkk'] = ''
        bc['dusty']['argh!'] = ''

        assert bc.keys() != dict(bc.items()).keys(), "A regular dict's key order should be different than a BuildoutConfig's"

        assert bc['dusty'].keys() != dict(bc['dusty'].items()).keys()

        fp = tempfile.NamedTemporaryFile()

        buildout_write(fp.name, bc)

        data = fp.read()

        assert data == """[buildout]
parts = 

[1section]
a = 1

[8section]
b = 3

[2section]
c = 4

[something]
d = 99eleven

[09876]
d = 
\tyes
\tagain

[dusty]
kkkkk = 
kkkk = 
k = 
kk = 
kkk = 
argh! = 

"""

    def test_write_complicated_config(self):
        bc = BuildoutConfig()

        sec = bc['buildout']
        sec['parts'] = ['eggs', 'django', 'pyzmq']
        sec['unzip'] = 'true'

        sec = bc['eggs']
        sec['recipe'] = 'zc.recipe.egg'
        sec['eggs'] = ['south==0.7.1', 'IPython']
        sec['extra-paths'] = ['${buildout:directory}/parts/django',
            '${buildout:directory}/parts/django-registration',
            '${buildout:directory}/greatbigcrane',
            '${buildout:directory}/parts/pyzmq']

        sec = bc['django']
        sec['settings'] = 'development'
        sec['recipe'] = 'djangorecipe'
        sec['version'] = '1.2.1'
        sec['eggs'] = '${eggs:eggs}'
        sec['project'] = 'greatbigcrane'
        sec['extra-paths'] = '${eggs:extra-paths}'
        sec['fcgi'] = 'True'
        sec['wsgi'] = 'True'

        sec = bc['pyzmq']
        sec['recipe'] = 'zerokspot.recipe.git'
        sec['repository'] = 'http://github.com/zeromq/pyzmq.git'
        sec['as_egg'] = 'True'

        fp = tempfile.NamedTemporaryFile()

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
settings = development
recipe = djangorecipe
version = 1.2.1
eggs = ${eggs:eggs}
project = greatbigcrane
extra-paths = ${eggs:extra-paths}
fcgi = True
wsgi = True

[pyzmq]
recipe = zerokspot.recipe.git
repository = http://github.com/zeromq/pyzmq.git
as_egg = True

"""

def mktmpcfg(cfg):
    fp = tempfile.NamedTemporaryFile()
    fp.write(cfg)
    fp.seek(0)

    return fp

simple_buildout_cfg = """[buildout]
parts = """

complicated_buildout_cfg = """[buildout]
parts = eggs django pyzmq
unzip = true

[eggs]
recipe = zc.recipe.egg
eggs =
    south==0.7.1
    IPython
extra-paths =
    ${buildout:directory}/parts/django
    ${buildout:directory}/parts/django-registration
    ${buildout:directory}/greatbigcrane
    ${buildout:directory}/parts/pyzmq

[django]
settings = development
recipe = djangorecipe
version = 1.2.1
eggs = ${eggs:eggs}
project = greatbigcrane
extra-paths = ${eggs:extra-paths}
fcgi = True
wsgi = True

[pyzmq]
recipe = zerokspot.recipe.git
repository = http://github.com/zeromq/pyzmq.git
as_egg = True"""
