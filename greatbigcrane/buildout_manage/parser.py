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

import re

whitespace = re.compile(r'\s+')

class BuildoutConfig(SortedDict):
    """
    Represents a buildout.cfg
    """

    def __getitem__(self, key):
        if not self.__contains__(key):
            self[key] = SortedDict()
        return super(BuildoutConfig, self).__getitem__(key)

    def sections_with_key(self, key):
        """
        Get a list of section names that have a given key.

        For example:
        [buildout]
        eggs = myeggs

        [django]
        eggs = myeggs2

        [boo]
        noeggs = nothing

        sections_with_key['eggs'] will return [buildout, django]
        """

        return [section_name for section_name, section in self.iteritems() if key in section]

    def sanitize_parts_list(self):
        parts_list = self['buildout'].setdefault('parts', [])
        if not isinstance(parts_list, list):
            if parts_list:
                parts_list = [parts_list]
            else:
                parts_list = []
        exploded_parts_list = []
        for elem in parts_list:
            if whitespace.search(elem):
                exploded_parts_list += whitespace.split(elem)
            else:
                exploded_parts_list.append(elem)
        self['buildout']['parts'] = exploded_parts_list

    def remove_part(self, section_name):
        self.sanitize_parts_list()
        parts_list = self['buildout']['parts']
        if section_name in parts_list:
            parts_list.remove(section_name)

    def add_part(self, section_name):
        self.sanitize_parts_list()
        parts_list = self['buildout']['parts']
        if section_name not in parts_list:
            parts_list.append(section_name)

def buildout_parse(filename):
    """
    Given a filename, parse the buildout config and return a BuildoutConfig object that represents it
    """
    parser = RawConfigParser(dict_type=SortedDict)

    # Don't ask me, buildout had it...
    parser.optionxform = lambda s: s

    if isinstance(filename, basestring):
        parser.read(filename)
    else:
        parser.readfp(filename)

    config = BuildoutConfig()

    for section in parser.sections():
        for key, value in parser.items(section):
            value = value.strip()
            if '\n' in value:
                value = [x for x in value.split('\n') if x]
            config[section][key] = value

    config.sanitize_parts_list()

    return config

def buildout_write(fp, config):
    """
    Given a filename and a BuildoutConfig, write the contents of the BuildoutConfig to the file
    """

    if isinstance(fp, basestring):
        fp = open(fp, "w")
        close = True
    else:
        close = False

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
    if close:
        fp.close()
