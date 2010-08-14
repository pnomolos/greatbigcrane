from django.db import models

make_choice = lambda x: ([(p,p) for p in x])

class Notification(models.Model):
    status = models.CharField(max_length=15, choices=make_choice([
        "success", "error", "general!"]))
    summary = models.CharField(max_length=128)
    message = models.TextField()
    notification_time = models.DateTimeField(auto_now_add=True)
