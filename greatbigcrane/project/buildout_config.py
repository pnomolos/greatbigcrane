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

    def __getitem__(self, key):
        if not self.__contains__(key):
            self[key] = SortedDict()
        return super(BuildoutConfig, self).__getitem__(key)

def buildout_parse(filename):
    """
    Given a filename, parse the buildout config and return a BuildoutConfig object that represents it
    """
    parser = RawConfigParser(dict_type=SortedDict)

    # Don't ask me, buildout had it...
    parser.optionxform = lambda s: s

    parser.read(filename)

    config = BuildoutConfig()

    for section in parser.sections():
        for key, value in parser.items(section):
            value = value.strip()
            if '\n' in value:
                value = value.split('\n')
            config[section][key] = value

    return config

def buildout_write(filename, config):
    """
    Given a filename and a BuildoutConfig, write the contents of the BuildoutConfig to the file
    """

    fp = open(filename, "w")

    parser = RawConfigParser(dict_type=SortedDict)

    # Don't ask me, buildout had it...
    parser.optionxform = lambda s: s

    for section in config:
        parser.add_section(section)
        for key, value in config[section].iteritems():
            if isinstance(value, list):
                value = '\n'.join([''] + value)
            parser.set(section, key, value)

    parser.write(fp)
    fp.close()
