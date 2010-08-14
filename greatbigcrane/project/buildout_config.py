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

from ConfigParser import RawConfigParser
from django.utils.datastructures import SortedDict

class BuildoutConfig(SortedDict):
    """
    Represents a buildout.cfg
    """

def buildout_parse(filename):
    parser = RawConfigParser(dict_type=SortedDict)

    # Don't ask me, buildout had it...
    parser.optionxform = lambda s: s

    parser.read(filename)

    config = BuildoutConfig()

    for section in parser.sections():
        config[section] = SortedDict()
        for key, value in parser.items(section):
            value = value.strip()
            if '\n' in value:
                value = value.split('\n')
            config[section][key] = value

    return config
