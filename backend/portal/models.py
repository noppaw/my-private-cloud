from django.db import models

class MicroApp(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=200, help_text="Ex: /weather or https://google.com")
    icon_name = models.CharField(max_length=50, default="image-application", help_text="Material Design Icon name")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
