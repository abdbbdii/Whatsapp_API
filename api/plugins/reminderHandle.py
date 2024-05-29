from api.whatsapp_api_handle import Message
import json

pluginInfo = {
    "command_name": "reminder",
    "description": "This is a reminder plugin.",
    "admin_privilege": False,
    "internal": True,
}


def handle_function(message: Message):
    for reminder in message.document["reminders_notified"]:
        notes = json.loads(reminder["notes"])
        match notes["time_remaining"]:
            case 0:
                message.outgoing_text_message = f'*⌛ Time\'s up for {reminder["title"]} ⌛*'
            case 10:
                message.outgoing_text_message = f'*🔔 Reminder: Only {notes["time_remaining"]} minutes left for {reminder["title"]}*\n\nYou should start submitting your work now.\n{notes["link"]}'
            case _:
                message.outgoing_text_message = f'*🔔 Reminder: Only {notes["time_remaining"]} minutes left for {reminder["title"]}*'
        message.send_message()
