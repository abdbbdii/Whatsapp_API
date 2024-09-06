import json
from datetime import datetime, timedelta

from api.whatsapp_api_handle import Message
from api.utils.reminders_api import ReminderAPI
from api.utils.download_gdrive import download_gdrive_file
from api.appSettings import appSettings

pluginInfo = {
    "command_name": "classroom",
    "description": "This is a classroom plugin.",
    "admin_privilege": False,
    "internal": True,
}

def preprocess(message: Message) -> None:
    if (message.document_type == "reminder_api" and str(message.document.get("application_id")) == appSettings.reminders_api_classroom_id) or message.document_type == "google_classroom_api":
        message.incoming_text_message = message.command_prefix + pluginInfo["command_name"]

def add_minutes(date: dict[str, int], time: dict[str, int], minutes: int):
    new_datetime = datetime(date.get("year", 0), date.get("month", 0), date.get("day", 0), time.get("hours", 0), time.get("minutes", 0)) + timedelta(minutes=minutes)
    return (
        {"year": new_datetime.year, "month": new_datetime.month, "day": new_datetime.day},
        {"hours": new_datetime.hour, "minutes": new_datetime.minute},
    )


def subtract_minutes(date: dict[str, int], time: dict[str, int], minutes: int):
    new_datetime = datetime(date.get("year", 0), date.get("month", 0), date.get("day", 0), time.get("hours", 0), time.get("minutes", 0)) - timedelta(minutes=minutes)
    return (
        {"year": new_datetime.year, "month": new_datetime.month, "day": new_datetime.day},
        {"hours": new_datetime.hour, "minutes": new_datetime.minute},
    )


def set_reminder(date: dict, time: dict, title: str, link: str):
    if not date:
        return
    if not time:
        time = {"hours": 23, "minutes": 59}
    reminders_api = ReminderAPI(appSettings.reminders_key, appSettings.public_url + "api/reminder", ("admin", "admin"))
    if appSettings.reminders_api_classroom_id and reminders_api.get_application(appSettings.reminders_api_classroom_id).json().get("message") != "Item not found.":
        application_id = appSettings.reminders_api_classroom_id
    else:
        application_id = reminders_api.find_application_id(appSettings.reminders_api_classroom_name)
        if not application_id:
            application_id = reminders_api.create_application(appSettings.reminders_api_classroom_name, "10:00").json().get("id")
        appSettings.update("reminders_api_classroom_id", application_id)

    time_intervals = [60, 30, 10, 0]
    for time_interval in time_intervals:
        date_tz, time_tz = subtract_minutes(date, time, time_interval)
        response = reminders_api.create_reminder(
            application_id=application_id,
            title=title,
            timezone="Asia/Karachi",
            date_tz=f'{date_tz["year"]}-{date_tz["month"]:02d}-{date_tz["day"]:02d}',
            time_tz=f'{time_tz["hours"]:02d}:{time_tz["minutes"]:02d}',
            notes=json.dumps({"time_remaining": time_interval, "link": link, "sender": appSettings.classroom_group_id}),
            rrule=None,
            webhook_url=appSettings.public_url + "api/reminder",
        )
        print(response.text)


def make_message(header, items, footer=""):
    message = f"*{header}*\n\n"
    items = {k: v for k, v in items.items() if v}
    message += "\n".join([f"*{k}*: {v}" for k, v in items.items()])
    if footer:
        message += f"\n\n_{footer}_"
    return message


def handle_function(message: Message):
    if message.document_type == "reminder_api":
        notes = json.loads(message.document["notes"])
        match notes["time_remaining"]:
            case 0:
                message.outgoing_text_message = f'*⌛ Time\'s up for {message.document["title"]} ⌛*'
                reminders_api = ReminderAPI(appSettings.reminders_key, appSettings.public_url + "api/reminder", ("admin", "admin"))
                print(reminders_api.delete_reminder(message.document["id"]).json())
            case 10:
                message.outgoing_text_message = f'*🔔 Only {notes["time_remaining"]} minutes left for {message.document["title"]} 🔔*\n\nYou should start submitting your work now.\n{notes["link"]}'
            case _:
                message.outgoing_text_message = f'*🔔 Only {notes["time_remaining"]} minutes left for {message.document["title"]} 🔔*'
        message.send_message()
        return

    elif message.document_type != "google_classroom_api":
        return

    if message.document["type"] == "courseWorkMaterial":
        message.outgoing_text_message = make_message(
            header=f'New Material for {message.document["course"]["descriptionHeading"]}',
            items={
                "📝 Title": message.document["activity"]["title"],
                "📄 Description": message.document["activity"].get("description"),
                "🔗 Link": message.document["activity"]["alternateLink"],
            },
        )

    elif message.document["type"] == "courseWork":
        if message.document["activity"].get("dueTime"):
            message.document["activity"]["dueDate"], message.document["activity"]["dueTime"] = add_minutes(message.document["activity"]["dueDate"], message.document["activity"]["dueTime"], 5 * 60)

        if time := message.document["activity"].get("dueTime"):
            time = f'{((time["hours"] - 12) if time["hours"] > 12 else time["hours"]):02d}:{time["minutes"]:02d} {"PM" if time["hours"] > 12 else "AM"}'
        else:
            time = ""

        if message.document["activity"].get("dueDate") is None:
            due = "No due date provided"
        else:
            due = f'{"/".join(list(map(str, message.document["activity"]["dueDate"].values())))} {time}'

        message.outgoing_text_message = make_message(
            header=f'New {message.document["activity"]["workType"].title()} created for {message.document["course"]["descriptionHeading"]}',
            items={
                "📝 Title": message.document["activity"]["title"],
                "📄 Description": message.document["activity"].get("description"),
                "⏰ Due": due,
                "🏆 Points": message.document["activity"].get("maxPoints"),
                "🔗 Link": message.document["activity"]["alternateLink"],
            },
            footer="Good Luck ✌️",
        )

    elif message.document["type"] == "announcements":
        message.outgoing_text_message = make_message(
            header=f'New Announcement for {message.document["course"]["descriptionHeading"]}',
            items={
                "💬 Text": message.document["activity"]["text"],
                "🔗 Link": message.document["activity"]["alternateLink"],
            },
        )
        message.document["activity"]["title"] = "Announcement"
    message.send_message()

    if message.document["activity"].get("dueDate"):
        set_reminder(
            message.document["activity"].get("dueDate"),
            message.document["activity"].get("dueTime"),
            message.document["activity"]["title"],
            message.document["activity"]["alternateLink"],
        )
    materials = message.document["activity"].get("materials")

    if not materials:
        return

    for i, material in enumerate(materials):
        if list(material.keys())[0] == "driveFile":
            message.outgoing_text_message = make_message(
                header=f'Material {i+1} of {len(materials)} for {message.document["activity"]["title"]}',
                items={
                    "📝 Title": material["driveFile"]["driveFile"]["title"],
                    "📄 Description": material["driveFile"]["driveFile"].get("description"),
                    "🔗 Link": material["driveFile"]["driveFile"]["alternateLink"],
                },
            )
            print(material["driveFile"]["driveFile"])
            gdrive_file = download_gdrive_file(material["driveFile"]["driveFile"]["alternateLink"])
            message.media = {"file": [material["driveFile"]["driveFile"]["title"], gdrive_file]}
            print("sending media")
            message.send_file()

        elif list(material.keys())[0] == "youtubeVideo":
            message.outgoing_text_message = make_message(
                header=f'Material {i+1} of {len(materials)} for {message.document["activity"]["title"]}',
                items={
                    "📝 Title": material["youtubeVideo"]["title"],
                    "🔗 YouTube Link": material["youtubeVideo"]["alternateLink"],
                },
            )
            message.send_message()

        elif list(material.keys())[0] == "link":
            message.outgoing_text_message = make_message(
                header=f'Material {i+1} of {len(materials)} for {message.document["activity"]["title"]}',
                items={
                    "📝 Title": material["link"]["title"],
                    "🔗 Link": material["link"]["url"],
                },
            )
            message.send_message()
