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

    def delete_reminders_for_application(self, application_id: str):
        reminders = self.get_reminders_for_application(application_id).json()["data"]
        for reminder in reminders:
            self.delete_reminder(reminder["id"])

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

    def delete_applications(self):
        applications = self.get_applications().json().get("data")
        for application in applications:
            self.delete_application(application["id"])

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

    def create_reminder(self, application_id: str, title: str, timezone: str, date_tz: str, time_tz: str, rrule: str = None, notes: str = None, webhook_url: str = None):
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
                "webhook_url": self.webhook_url if webhook_url is None else webhook_url,
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

    def delete_reminders(self):
        reminders = self.get_reminders().json()["data"]
        for reminder in reminders:
            self.delete_reminder(reminder["id"])

    def find_application_id(self, application_name: str):
        applications = self.get_applications().json()["data"]
        for application in applications:
            if application["name"] == application_name:
                return application["id"]
        return None


if __name__ == "__main__":
    reminder_api = ReminderAPI("jVgTHzQthB7V1WNZKlFwMeykVbGAfEB6tfI7Qgoy", "https://whatsapp-api-backend.vercel.app/", ("your_username", "your_password"))
    # print(reminder_api.create_application("classroom", "10:00").text)  # 873

    # print(reminder_api.create_application("Whatsapp_API_cronjob", "10:00").text)  # 874
    # print(reminder_api.create_reminder("876", "Whatsapp_API_Backend", "Asia/Karachi", "2024-05-29", "21:37", "FREQ=MINUTELY;INTERVAL=5", webhook_url="https://whatsapp-api-backend.vercel.app/").text)  # 16429
    # print(reminder_api.create_reminder("876", "Whatsapp_API_Client", "Asia/Karachi", "2024-05-29", "21:37", "FREQ=MINUTELY;INTERVAL=3", webhook_url="https://whatsapp-api-client-1.onrender.com/user/my/privacy").text)  # 16430
    # print(reminder_api.create_reminder("876", "Google_Classroom_API", "Asia/Karachi", "2024-05-29", "21:37", "FREQ=MINUTELY;INTERVAL=3", webhook_url="https://google-classroom-api.vercel.app/api/notify_new_activity").text)  # 16431

    # reminder_api.delete_reminders_for_application("873")
    # print(reminder_api.get_reminders_for_application("873").json())
    # print(reminder_api.get_applications().json())