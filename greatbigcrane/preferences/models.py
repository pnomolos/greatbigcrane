from django.db import models

class Preference(models.Model):
    name = models.CharField(max_length=32)
    value = models.CharField(max_length=512)
