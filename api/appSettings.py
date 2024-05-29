import os
from .models import Settings
from dotenv import load_dotenv, find_dotenv
from django.conf import settings as django_settings

load_dotenv(find_dotenv()) if not os.getenv("VERCEL_ENV") else None


class AppSettings:
    def __init__(self) -> None:
        settings_values = {}
        settings = Settings.objects.first()

        if not settings:
            settings = Settings()

        for field in settings._meta.fields:
            value = getattr(settings, field.name)
            if not value or value == "":
                value = os.getenv(field.name.upper())
                if value:
                    setattr(settings, field.name, value)

            settings_values[field.name] = value

        settings.save()

        self.whatsapp_client_url = settings.whatsapp_client_url_test if django_settings.DEBUG else settings.whatsapp_client_url
        self.public_url = settings.public_url_test if django_settings.DEBUG else settings.public_url
        self.admin_ids = settings.admin_ids.split(",")
        self.blacklist_ids = settings.blacklist_ids.split(",")
        self.admin_command_prefix = settings.admin_command_prefix
        self.classroom_group_id = settings.classroom_group_id_test if django_settings.DEBUG else settings.classroom_group_id
        self.reminders_api_classroom_id = settings.reminders_api_classroom_id
        self.reminders_key = settings.reminders_key
        self.token_pickle_base64 = settings.token_pickle_base64
        self.google_credentials = settings.google_credentials

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
google_credentials: {self.google_credentials}"""

    def update(self, key, value):
        setattr(self, key, value)
        settings = Settings.objects.first()

        if isinstance(getattr(settings, key), list):
            value = ",".join(value)

        setattr(settings, key, value)
        settings.save()

    def append(self, key, value):
        getattr(self, key).append(value)
        settings = Settings.objects.first()
        setattr(settings, key, ",".join(getattr(self, key)))
        settings.save()

    def remove(self, key, value):
        getattr(self, key).remove(value)
        settings = Settings.objects.first()
        setattr(settings, key, ",".join(getattr(self, key)))
        settings.save()

    def empty(self):

        for field in self.__dict__:
            setattr(self, field, "")

        settings = Settings.objects.first()

        for field in settings._meta.fields:
            if field.name != "id":
                setattr(settings, field.name, "")

        settings.save()

# class AppSettings:
#     def __init__(self) -> None:
#         self.whatsapp_client_url = ""
#         self.public_url = ""
#         self.admin_ids = ""
#         self.blacklist_ids = ""
#         self.admin_command_prefix = ""
#         self.classroom_group_id = ""
#         self.reminders_api_classroom_id = ""
#         self.reminders_key = ""
#         self.token_pickle_base64 = ""
#         self.google_credentials = ""

appSettings = AppSettings()