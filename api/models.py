from django.db import models
from datetime import timedelta


class Settings(models.Model):
    admin_ids = models.TextField(default=None, null=True)
    whatsapp_client_url = models.TextField(default=None, null=True)
    whatsapp_client_url_test = models.TextField(default=None, null=True)
    public_url = models.TextField(default=None, null=True)
    public_url_test = models.TextField(default=None, null=True)
    blacklist_ids = models.TextField(default=None, null=True)
    admin_command_prefix = models.TextField(default=None, null=True)
    classroom_group_id = models.TextField(default=None, null=True)
    classroom_group_id_test = models.TextField(default=None, null=True)
    reminders_api_classroom_id = models.TextField(default=None, null=True)
    reminders_api_classroom_id_test = models.TextField(default=None, null=True)
    reminders_api_classroom_name = models.TextField(default=None, null=True)
    reminders_api_classroom_name_test = models.TextField(default=None, null=True)
    reminders_key = models.TextField(default=None, null=True)
    token_pickle_base64 = models.TextField(default=None, null=True)
    ocr_space_api_key = models.TextField(default=None, null=True)
    openai_api_key = models.TextField(default=None, null=True)
    kharchey_group_id = models.TextField(default=None, null=True)
    reminders_api_remind_id = models.TextField(default=None, null=True)
    utils_server_url = models.TextField(default=None, null=True)
    utils_server_password = models.TextField(default=None, null=True)
    last_outgoing_message_time = models.DateTimeField(auto_now_add=True, null=True)
    last_outgoing_message = models.TextField(default=None, null=True)


class Kharchey(models.Model):
    item = models.TextField(default=None, null=True)
    quantity = models.IntegerField(default=0, null=True)
    price = models.IntegerField(default=0, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    group = models.TextField(default=None, null=True)
    sender = models.TextField(default=None, null=True)

    def save(self, *args, **kwargs):
        if self.date is not None:
            self.date += timedelta(hours=5)
        super(Kharchey, self).save(*args, **kwargs)


class GPTResponse(models.Model):
    message = models.TextField(default=None, null=True)
    response = models.TextField(default=None, null=True)
    group = models.TextField(default=None, null=True)
    sender = models.TextField(default=None, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        if self.date is not None:
            self.date += timedelta(hours=5)
        super(GPTResponse, self).save(*args, **kwargs)


class Users(models.Model):
    user_id = models.TextField(default=None, null=True)
    group_id = models.TextField(default=None, null=True)
    description = models.JSONField(default=None, null=True)
