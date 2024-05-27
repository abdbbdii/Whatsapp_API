from api.whatsapp_api_handle import appSettings, Message
import json

pluginInfo = {
    "command_name": "reminder",
    "description": "This is a reminder plugin.",
    "admin_privilege": False,
    "internal": True,
}

def handle_function(message: Message):
    for reminder in message.document["reminders_notified"]:
        print(reminder["notes"])
        notes = json.loads(reminder["notes"])
        if notes["time_remaining"] == 0:
            message.outgoing_text_message = f'*🔔 Reminder: Time\'s up for \"{reminder["title"]}\"*'
        elif notes["time_remaining"] == 10:
            message.outgoing_text_message = f'*🔔 Reminder: Only {notes["time_remaining"]} minutes left for \"{reminder["title"]}\"*\n\nYou should start sbmitting your work now.\n\n{notes["link"]}'
        else:
            message.outgoing_text_message = f'*🔔 Reminder: Only {notes["time_remaining"]} minutes left for \"{reminder["title"]}\"*'
        message.send_message()