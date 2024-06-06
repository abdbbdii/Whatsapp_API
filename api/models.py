from django.db import models
from datetime import timedelta


class Settings(models.Model):
    admin_ids = models.TextField(default="", null=True)
    whatsapp_client_url = models.TextField(default="", null=True)
    whatsapp_client_url_test = models.TextField(default="", null=True)
    public_url = models.TextField(default="", null=True)
    public_url_test = models.TextField(default="", null=True)
    blacklist_ids = models.TextField(default="", null=True)
    admin_command_prefix = models.TextField(default="", null=True)
    classroom_group_id = models.TextField(default="", null=True)
    classroom_group_id_test = models.TextField(default="", null=True)
    reminders_api_classroom_id = models.TextField(default="", null=True)
    reminders_api_classroom_id_test = models.TextField(default="", null=True)
    reminders_api_classroom_name = models.TextField(default="", null=True)
    reminders_api_classroom_name_test = models.TextField(default="", null=True)
    reminders_key = models.TextField(default="", null=True)
    token_pickle_base64 = models.TextField(default="", null=True)
    google_credentials = models.TextField(default="", null=True)
    ocr_space_api_key = models.TextField(default="", null=True)
    openai_api_key = models.TextField(default="", null=True)
    kharchey_group_id = models.TextField(default="", null=True)

class Kharchey(models.Model):
    item = models.TextField(default="", null=True)
    quantity = models.IntegerField(default=0, null=True)
    price = models.IntegerField(default=0, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    group = models.TextField(default="", null=True)
    sender = models.TextField(default="", null=True)

    def save(self, *args, **kwargs):
        if self.date is not None:
            self.date += timedelta(hours=5)
        super(Kharchey, self).save(*args, **kwargs)