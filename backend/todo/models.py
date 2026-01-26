from django.db import models

class Task(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(null=True, blank=True) 
    end_time = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    is_template = models.BooleanField(default=False)
    notify_telegram = models.BooleanField(default=True)
    is_notification_sent = models.BooleanField(default=False)
    color = models.CharField(max_length=7, default='#3B82F6')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title