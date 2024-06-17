from api.utils.reminders_api import ReminderAPI
from api.whatsapp_api_handle import Message
from api.appSettings import appSettings

pluginInfo = {
    "command_name": "remind",
    "description": "Set a reminder for a specific date and time.",
    "admin_privilege": False,
    "internal": False,
}


def handle_function(message: Message):
    reminders_api = ReminderAPI(appSettings.reminders_key, appSettings.public_url + "api/reminder", ("admin", "admin"))
    if appSettings.reminders_api_remind_id and reminders_api.get_application(appSettings.reminders_api_remind_id).json().get("message") != "Item not found.":
        application_id = appSettings.reminders_api_remind_id
    else:
        application_id = reminders_api.find_application_id(appSettings.reminders_api_classroom_name)
        if not application_id:
            application_id = reminders_api.create_application(appSettings.reminders_api_classroom_name, "10:00").json().get("id")
        appSettings.update("reminders_api_remind_id", application_id)
        
    date_tz, time_tz = subtract_minutes(date, time, reminder)
    response = reminders_api.create_reminder(
        application_id=application_id,
        title=title,
        timezone="Asia/Karachi",
        date_tz=f'{date_tz["year"]}-{date_tz["month"]:02d}-{date_tz["day"]:02d}',
        time_tz=f'{time_tz["hours"]:02d}:{time_tz["minutes"]:02d}',
        notes=json.dumps({"from": "remind"}),
        rrule=None,
        webhook_url=appSettings.public_url + "api/reminder",
    )
    print(response.text)
