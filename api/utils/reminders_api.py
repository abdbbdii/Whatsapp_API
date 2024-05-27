import requests

class ReminderAPI:
    def __init__(self, key: str, webhook_url: str = None, http_basic_auth: tuple | list = None) -> None:
        self.key = key
        self.__headers = {
            "Authorization": "Bearer " + key,
        }
        self.endpoint = "https://reminders-api.com/api"
        self.webhook_url = webhook_url
        self.http_basic_auth = http_basic_auth

    def get_user(self):
        return requests.get(
            f"{self.endpoint}/user",
            headers=self.__headers,
        )

    def get_applications(self):
        return requests.get(
            f"{self.endpoint}/applications/",
            headers=self.__headers,
        )

    def get_application(self, application_id: str):
        return requests.get(
            f"{self.endpoint}/applications/{application_id}",
            headers=self.__headers,
        )

    def get_reminders_for_application(self, application_id: str):
        return requests.get(
            f"{self.endpoint}/applications/{application_id}/reminders",
            headers=self.__headers,
        )

    def create_application(self, name: str, default_reminder_time_tz: str):
        return requests.post(
            f"{self.endpoint}/applications/",
            headers=self.__headers,
            data={
                "name": name,
                "default_reminder_time_tz": default_reminder_time_tz,
                "webhook_url": self.webhook_url,
                "http_basic_auth_username": self.http_basic_auth[0],
                "http_basic_auth_password": self.http_basic_auth[1],
            },
        )

    def update_application(self, application_id: str, name: str, default_reminder_time_tz: str):
        return requests.put(
            f"{self.endpoint}/applications/{application_id}",
            headers=self.__headers,
            data={
                "name": name,
                "default_reminder_time_tz": default_reminder_time_tz,
                "webhook_url": self.webhook_url,
                "http_basic_auth_username": self.http_basic_auth[0],
                "http_basic_auth_password": self.http_basic_auth[1],
            },
        )

    def delete_application(self, application_id: str):
        return requests.delete(
            f"{self.endpoint}/applications/{application_id}",
            headers=self.__headers,
        )

    def get_reminders(self):
        return requests.get(
            f"{self.endpoint}/reminders",
            headers=self.__headers,
        )

    def get_reminder(self, reminder_id: str):
        return requests.get(
            f"{self.endpoint}/reminders/{reminder_id}",
            headers=self.__headers,
        )

    def create_reminder(self, application_id: str, title: str, timezone: str, date_tz: str, time_tz: str, rrule: str = None, notes: str = None):
        return requests.post(
            f"{self.endpoint}/applications/{application_id}/reminders/",
            headers=self.__headers,
            data={
                "title": title,
                "timezone": timezone,
                "date_tz": date_tz,
                "time_tz": time_tz,
                "rrule": rrule,
                "notes": notes,
                "webhook_url": self.webhook_url,
                "http_basic_auth_username": self.http_basic_auth[0],
                "http_basic_auth_password": self.http_basic_auth[1],
            },
        )

    def update_reminder(self, reminder_id: str, title: str, timezone: str, date_tz: str, time_tz: str, rrule: str):
        return requests.put(
            f"{self.endpoint}/reminders/{reminder_id}",
            headers=self.__headers,
            data={
                "title": title,
                "timezone": timezone,
                "date_tz": date_tz,
                "time_tz": time_tz,
                "rrule": rrule,
                "webhook_url": self.webhook_url,
                "http_basic_auth_username": self.http_basic_auth[0],
                "http_basic_auth_password": self.http_basic_auth[1],
            },
        )

    def delete_reminder(self, reminder_id: str):
        return requests.delete(
            f"{self.endpoint}/reminders/{reminder_id}",
            headers=self.__headers,
        )

    def find_application_id(self, application_name: str):
        applications = self.get_applications().json()["data"]
        for application in applications:
            if application["name"] == application_name:
                return application["id"]
        return None


# get_user()

# create_application("My Application", "10:00", "https://whatsapp-api.serveo.net/api/reminder", "your_username", "your_password")
# get_applications()
# get_application()
# get_reminders_for_application("859")
# delete_application("858")

# create_reminder("859", "Weekly Team Meeting", "Europe/London", "2024-06-01", "10:00", "FREQ=WEEKLY;BYDAY=MO", "https://whatsapp-api.serveo.net/api/reminder", "your_username", "your_password")
# get_reminders()
# get_reminder()
# delete_reminder("16367")
