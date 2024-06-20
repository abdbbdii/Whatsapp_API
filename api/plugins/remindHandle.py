import json
from argparse import ArgumentParser

import phonenumbers

from api.utils.reminders_api import ReminderAPI
from api.whatsapp_api_handle import Message
from api.appSettings import appSettings

pluginInfo = {
    "command_name": "remind",
    "description": "Set a reminder for a specific date and time.",
    "admin_privilege": False,
    "internal": False,
}


def get_timezone_from_number(phone_number: str, country_code_to_timezone: dict) -> str | None:
    try:
        parsed_number = phonenumbers.parse(phone_number)
        country_code = phonenumbers.region_code_for_number(parsed_number)
        timezone = country_code_to_timezone.get(country_code, "Unknown timezone")
        return timezone
    except phonenumbers.phonenumberutil.NumberParseException:
        return None


def handle_function(message: Message):
    if message.document_type == "reminder_api":
        message.outgoing_text_message = f"Reminder: {message.document['title']}"
        message.send_message()
        return
    try:
        if len(message.arguments) == 1:
            raise SystemExit
        parsed = parser(message.arguments[1:])

    except SystemExit:
        pretext = message.command_prefix + (appSettings.admin_command_prefix + " " if pluginInfo["admin_privilege"] else "") + pluginInfo["command_name"]
        message.outgoing_text_message = f"""*Usage:*
- Reminder: `{pretext} -d [YYYY-MM-DD] -t [HH:MM] -m [message]`
- Reminder with recurrence rule: `{pretext} -d [YYYY-MM-DD] -t [HH:MM] -r [RRULE] -m [message]`
"""
        message.send_message()
        return

    reminders_api = ReminderAPI(appSettings.reminders_key, appSettings.public_url + "api/reminder", ("admin", "admin"))
    if appSettings.reminders_api_remind_id and reminders_api.get_application(appSettings.reminders_api_remind_id).json().get("remind") != "Item not found.":
        application_id = appSettings.reminders_api_remind_id
    else:
        application_id = reminders_api.find_application_id("remind")
        if not application_id:
            application_id = reminders_api.create_application("remind", "10:00").json().get("id")
        appSettings.update("reminders_api_remind_id", application_id)

    if timezone := get_timezone_from_number("+" + message.sender, json.load(open("api/assets/timezones.json"))):
        response = reminders_api.create_reminder(
            application_id=application_id,
            title=' '.join(parsed.message),
            timezone=timezone,
            date_tz=parsed.date,
            time_tz=parsed.time,
            notes=json.dumps({"sender": message.sender}),
            rrule=parsed.rrule,
            webhook_url=appSettings.public_url + "api/reminder",
        )
        print(response.text)
        if error:=json.loads(response.text).get("errors"):
            message.outgoing_text_message = f"Error: {error}"
        else:
            message.outgoing_text_message = "Reminder set successfully."
    else:
        message.outgoing_text_message = "Could not determine timezone from phone number."

    message.send_message()


def parser(args: str) -> ArgumentParser:
    parser = ArgumentParser(description="Set a reminder for a specific date and time.")
    parser.add_argument("-d", "--date", type=str, help="Date in the format YYYY-MM-DD.")
    parser.add_argument("-t", "--time", type=str, help="Time in the format HH:MM.")
    parser.add_argument("-r", "--rrule", type=str, help="Recurrence rule.")
    parser.add_argument("-m", "--message", type=str, nargs='+', help="Message to remind.")
    return parser.parse_args(args)
