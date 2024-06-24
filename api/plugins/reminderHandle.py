import json
from argparse import ArgumentParser

from api.appSettings import appSettings
from api.whatsapp_api_handle import Message, SendHelp
from api.utils.reminders_api import ReminderAPI

pluginInfo = {
    "command_name": "reminder",
    "description": "Set a reminder for a specific date and time.",
    "admin_privilege": False,
    "internal": False,
}

helpMessage = {
    "commands": [
        {
            "command": "create -d [YYYY-MM-DD] -t [HH:MM] -m [message]",
            "description": "Set a reminder for a specific date and time.",
            "examples": [
                "create -d 2022-12-31 -t 23:59 -m Happy New Year!",
            ],
        },
        {
            "command": "create -d [YYYY-MM-DD] -t [HH:MM] -r [RRULE] -m [message]",
            "description": "Set a reminder for a specific date and time with recurrence rule.",
            "examples": [
                "create -d 2022-12-31 -t 23:59 -r FREQ=YEARLY -m Happy New Year!",
            ],
        },
        {
            "command": "delete [reminder_id] [reminder_id] ...",
            "description": "Delete reminders.",
            "examples": [
                "delete 1 2",
            ],
        },
        {
            "command": "get",
            "description": "Get reminders.",
        },
    ],
    "note": "Reminders are set based on the phone number of the sender.",
}


def preprocess(message: Message) -> None:
    if message.document_type == "reminder_api" and str(message.document.get("application_id")) == appSettings.reminders_api_remind_id:
        message.incoming_text_message = message.command_prefix + pluginInfo["command_name"]


def create_reminder(message: Message, reminders_api: ReminderAPI):
    if message.timezone:
        parsed = craete_parser(message.arguments[2:])
        response = reminders_api.create_reminder(
            application_id=appSettings.reminders_api_remind_id,
            title=" ".join(parsed.message),
            timezone=message.timezone,
            date_tz=parsed.date,
            time_tz=parsed.time,
            notes=json.dumps({"sender": message.sender}),
            rrule=parsed.rrule,
            webhook_url=appSettings.public_url + "api/reminder",
        )
        print(response.text)
        if error := json.loads(response.text).get("errors"):
            message.outgoing_text_message = f"Error: {error}"
        else:
            message.outgoing_text_message = "Reminder set successfully."
    else:
        message.outgoing_text_message = "Could not determine timezone from phone number."

    message.send_message()


def get_reminders(message: Message, reminders_api: ReminderAPI):
    if len(message.arguments) > 2:
        raise SystemExit
    response = reminders_api.get_reminders_for_application(appSettings.reminders_api_remind_id)
    print(response.text)
    if error := json.loads(response.text).get("errors"):
        message.outgoing_text_message = f"Error: {error}"
    elif reminders := [reminder for reminder in json.loads(response.text).get("data") if json.loads(reminder.get("notes")).get("sender") == message.sender]:
        message.outgoing_text_message = "*Reminders:*\n"
        message.outgoing_text_message += "\n".join([f"{reminder.get('id')}: {reminder.get('title')}" for reminder in reminders])
    else:
        message.outgoing_text_message = "No reminders found."
    message.send_message()


def delete_reminder(message: Message, reminders_api: ReminderAPI):
    success = []
    failure = []
    for reminder_id in message.arguments[2:]:
        response = reminders_api.delete_reminder(reminder_id)
        print(response.text)
        if error := json.loads(response.text).get("message") == "Item not found.":
            failure.append((reminder_id, error))
        else:
            success.append(reminder_id)
    if success:
        message.outgoing_text_message = f"Successfully deleted reminders: {', '.join(success)}\n"
    if failure:
        message.outgoing_text_message += f"Failed to delete reminders: {', '.join([f'{reminder_id}: {error}' for reminder_id, error in failure])}\n"
    if message.outgoing_text_message:
        message.send_message()
    else:
        raise SystemExit


def handle_function(message: Message):
    if message.document_type == "reminder_api":
        message.outgoing_text_message = message.document["title"]
        message.send_message()
    else:
        reminders_api = ReminderAPI(appSettings.reminders_key, appSettings.public_url + "api/reminder", ("admin", "admin"))
        if appSettings.reminders_api_remind_id and reminders_api.get_application(appSettings.reminders_api_remind_id).json().get("remind") != "Item not found.":
            application_id = appSettings.reminders_api_remind_id
        else:
            application_id = reminders_api.find_application_id("remind")
            if not application_id:
                application_id = reminders_api.create_application("remind", "10:00").json().get("id")
            appSettings.update("reminders_api_remind_id", application_id)

        try:
            if len(message.arguments) == 1:
                raise SystemExit
            match message.arguments[1]:
                case "create":
                    create_reminder(message, reminders_api)
                case "delete":
                    delete_reminder(message, reminders_api)
                case "get":
                    get_reminders(message, reminders_api)
                case _:
                    raise SendHelp
        except SystemExit:
            raise SendHelp


def craete_parser(args: str) -> ArgumentParser:
    parser = ArgumentParser(description="Set a reminder for a specific date and time.")
    parser.add_argument("-d", "--date", type=str, help="Date in the format YYYY-MM-DD.")
    parser.add_argument("-t", "--time", type=str, help="Time in the format HH:MM.")
    parser.add_argument("-r", "--rrule", type=str, help="Recurrence rule.")
    parser.add_argument("-m", "--message", type=str, nargs="+", help="Message to remind.")
    return parser.parse_args(args)
