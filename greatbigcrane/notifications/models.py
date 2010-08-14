from django.db import models

make_choice = lambda x: ([(p,p) for p in x])

class Notification(models.Model):
    status = models.CharField(max_length=15, choices=make_choice([
        "success", "error", "general!"]))
    message = models.TextField()
