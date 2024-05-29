from django.db import models


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
    reminders_key = models.TextField(default="", null=True)
    token_pickle_base64 = models.TextField(default="", null=True)
    google_credentials = models.TextField(default="", null=True)