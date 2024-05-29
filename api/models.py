from django.db import models
from Whatsapp_API.settings import DEBUG
import os


class Settings(models.Model):
    admin_ids = models.TextField()
    whatsapp_client_url = models.TextField()
    public_url = models.TextField()
    blacklist_ids = models.TextField()
    admin_command_prefix = models.TextField()
    classroom_group_id = models.TextField()
    reminders_api_classroom_id = models.TextField()
    reminders_key = models.TextField()
    token_pickle_base64 = models.TextField()
    google_credentials = models.TextField()

    def __str__(self) -> str:
        return f"""admin_ids: {self.admin_ids}
whatsapp_client_url: {self.whatsapp_client_url}
public_url: {self.public_url}
blacklist_ids: {self.blacklist_ids}
admin_command_prefix: {self.admin_command_prefix}
classroom_group_id: {self.classroom_group_id}
reminders_api_classroom_id: {self.reminders_api_classroom_id}
reminders_key: {self.reminders_key}
token_pickle_base64: {self.token_pickle_base64}
google_credentials: {self.google_credentials}
"""

    def get_admin_ids(self):
        return self.admin_ids.split(",")

    def get_blacklist_ids(self):
        return self.blacklist_ids.split(",")

    def update(self, key, value):
        setattr(self, key, value)
        self.save()

    @staticmethod
    def load():
        if not Settings.objects.first():
            settings = Settings()
            settings.admin_ids = os.getenv("ADMIN_IDS").split(",")
            settings.whatsapp_client_url = os.getenv("WHATSAPP_CLIENT_URL_TEST") if DEBUG else os.getenv("WHATSAPP_CLIENT_URL")
            settings.public_url = os.getenv("PUBLIC_URL_TEST") if DEBUG else os.getenv("PUBLIC_URL")
            settings.blacklist_ids = os.getenv("BLACKLIST_IDS").split(",")
            settings.admin_command_prefix = os.getenv("ADMIN_COMMAND_PREFIX")
            settings.classroom_group_id = os.getenv("CLASSROOM_GROUP_ID_TEST") if DEBUG else os.getenv("CLASSROOM_GROUP_ID")
            settings.reminders_api_classroom_id = os.getenv("REMINDERS_API_CLASSROOM_ID")
            settings.reminders_key = os.getenv("REMINDERS_KEY")
            settings.token_pickle_base64 = os.getenv("TOKEN_PICKLE_BASE64")
            settings.google_credentials = os.getenv("GOOGLE_CREDENTIALS")
            settings.save()
        return Settings.objects.first()
