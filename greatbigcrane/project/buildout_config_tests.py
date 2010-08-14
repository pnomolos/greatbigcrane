from django.test import TestCase
from django.template import Template, RequestContext

from greatbigcrane.project.buildout_config import buildout_parse

"""
Notes:
* *Parse simplest buildout.cfg*
* Parse more complicated buildout.cfg

* Write simplest buildout.cfg
* Write more complicated buildout.cfg
"""

class BuildoutParse(TestCase):
    """Tests for buildout_parse module"""

    def test_parse_simplest_buildout(self):
        buildout_cfg = """[buildout]
develop = ."""

        buildout_object = buildout_parse(buildout_cfg)

        assert buildout_object['buildout']['develop'] == '.'
