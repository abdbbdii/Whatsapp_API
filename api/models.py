from django.db import models

class Settings(models.Model):
    settings_json = models.JSONField()