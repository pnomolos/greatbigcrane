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

from django.db import models

class PreferenceManager(models.Manager):
    def get_preference(self, name, default=None):
        try:
            return Preference.objects.get(name="projects_directory").value
        except Preference.DoesNotExist:
            return default

class Preference(models.Model):
    name = models.CharField(max_length=32, unique=True)
    value = models.CharField(max_length=512)
    help_text = models.CharField(max_length=512)
    objects = PreferenceManager()

    def __unicode__(self):
        return self.name
