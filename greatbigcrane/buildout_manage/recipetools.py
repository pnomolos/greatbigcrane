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

def add_parts(config, section_name):
    parts_list = config['buildout'].setdefault('parts', [])
    if section_name not in parts_list:
        parts_list.append(section_name)

section_re = re.compile(r'\${([^:]*):([^}]*)}')

def simple_property_get(name):
    def get(self):
        # Parse ${
        def convert_value(data):
            if data.startswith('${'):
                g = section_re.match(data)
                return (g.group(1), g.group(2))
            return data

        value = self.section[name]
        if isinstance(value, list):
            value = [convert_value(x) for x in value]
        else:
            value = convert_value(value)
        return value
    return get

def simple_property_set(name):
    def set(self, value):
        def convert_value(data):
            if isinstance(data, tuple):
                data = '${%s:%s}' % data
            return data

        if isinstance(value, list):
            value = [convert_value(x) for x in value]
        else:
            value = convert_value(value)
        self.section[name] = value
    return set

def simple_property_delete(name):
    def delete(self):
        del self.section[name]
    return delete

simple_property = lambda name: property(simple_property_get(name), simple_property_set(name), simple_property_delete(name))

def bool_property_get(name):
    def get(self):
        value = self.section[name]
        if value.lower() == 'true':
            return True
        return False
    return get

def bool_property_set(name):
    def set(self, value):
        if value == True:
            value = 'True'
        else:
            value = 'False'
        self.section[name] = value
    return set

bool_property = lambda name: property(bool_property_get(name), bool_property_set(name), simple_property_delete(name))
