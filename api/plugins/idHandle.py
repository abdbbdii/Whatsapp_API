from api.whatsapp_api_handle import Message
from api.appSettings import appSettings
from argparse import ArgumentParser

pluginInfo = {
    "command_name": "id",
    "admin_privilege": False,
    "description": "Find out the ID of a user or a group.",
    "internal": False,
}


def handle_function(message: Message):
    message.outgoing_text_message = f"ID: {message.send_to[0]}"
    message.send_message()