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

import re

section_re = re.compile(r'\${([^:]*):([^}]*)}')

def expand_value(value):
    """
    Converts ${buildout:directory}/something/something into
    (('buildout', 'directory'), '/something/something)
    """
    tokens = section_re.split(value)
    token_list = []
    if tokens[0]:
        token_list.append(tokens[0])
    steps = (len(tokens) - 1)/3
    for step in range(steps):
        token_list.append(tuple(tokens[step*3+1:step*3+3]))
        if tokens[step*3+3]:
            token_list.append(tokens[step*3+3])
    return tuple(token_list)

def compress_value(value):
    """
    Converts (('buildout', 'directory'), '/something/something) into
    ${buildout:directory}/something/something
    """
    data_list = []
    for elem in value:
        if isinstance(elem, tuple):
            data_list.append('${%s:%s}' % elem)
        else:
            data_list.append(elem)
    return ''.join(data_list)

def simple_property_get(name):
    def get(self):
        if name not in self.section:
            return ''
        value = self.section[name]
        return value
    return get

def simple_property_set(name):
    def set(self, value):
        self.section[name] = value
    return set

def simple_property_delete(name):
    def delete(self):
        if name in self.section:
            del self.section[name]
    return delete

simple_property = lambda name: property(simple_property_get(name), simple_property_set(name), simple_property_delete(name))

def bool_property_get(name):
    def get(self):
        if name not in self.section:
            return ''
        value = self.section[name]
        if value.lower() == 'true':
            return True
        return False
    return get

def bool_property_set(name):
    def set(self, value):
        if value == True:
            value = 'true'
        else:
            value = 'false'
        self.section[name] = value
    return set

bool_property = lambda name: property(bool_property_get(name), bool_property_set(name), simple_property_delete(name))
