from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=32)
    base_directory = models.CharField(max_length=512)
    description = models.TextField()
