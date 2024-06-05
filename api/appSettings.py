import os
from .models import Settings
from dotenv import load_dotenv, find_dotenv
from django.conf import settings as django_settings
from django.db.utils import ProgrammingError

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
        self.reminders_api_classroom_id = settings.reminders_api_classroom_id_test if django_settings.DEBUG else settings.reminders_api_classroom_id
        self.reminders_api_classroom_name = settings.reminders_api_classroom_name_test if django_settings.DEBUG else settings.reminders_api_classroom_name
        self.reminders_key = settings.reminders_key
        self.token_pickle_base64 = settings.token_pickle_base64
        self.google_credentials = settings.google_credentials
        self.ocr_space_api_key = settings.ocr_space_api_key
        self.openai_api_key = settings.openai_api_key

    def __str__(self) -> str:
        return "\n".join([f"{attr}: {getattr(self, attr)}" for attr in self.list()])

    def update(self, key: str, value: str):
        if isinstance(getattr(self, key), list):
            setattr(self, key, value.split(","))
        else:
            setattr(self, key, value)

        settings = Settings.objects.first()
        
        if key in ["whatsapp_client_url", "public_url", "classroom_group_id", "reminders_api_classroom_id", "reminders_api_classroom_name"]:
            if django_settings.DEBUG:
                key += "_test"

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

    def list(self):
        return [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

    def dict(self):
        return {attr: getattr(self, attr) for attr in self.list()}


try:
    appSettings = AppSettings()
except ProgrammingError:

    class AppSettings:
        def __init__(self) -> None:
            self.whatsapp_client_url = ""
            self.public_url = ""
            self.admin_ids = ""
            self.blacklist_ids = ""
            self.admin_command_prefix = ""
            self.classroom_group_id = ""
            self.reminders_api_classroom_id = ""
            self.reminders_key = ""
            self.token_pickle_base64 = ""
            self.google_credentials = ""
            self.ocr_space_api_key = ""
            self.openai_api_key = ""

    appSettings = AppSettings()
