from django.db import models
from django.core.urlresolvers import reverse


class Project(models.Model):
    name = models.CharField(max_length=32)
    base_directory = models.CharField(max_length=512)
    git_repo = models.CharField(max_length=512, blank=True, default='')
    description = models.TextField()

    def get_absolute_url(self):
        return reverse("view_project", args=[self.id])
