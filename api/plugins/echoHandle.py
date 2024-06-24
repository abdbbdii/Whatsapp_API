from api.whatsapp_api_handle import Message, SendHelp
from api.appSettings import appSettings
from argparse import ArgumentParser
from requests import get

pluginInfo = {
    "command_name": "echo",
    "admin_privilege": False,
    "description": "Echoes the message.",
    "internal": False,
}

helpMessage = {
    "commands": [
        {
            "command": "[message]",
            "description": "Echo message.",
            "examples": [
                "Hello!",
                "This is a test message.",
            ],
        },
        {
            "command": "[caption]",
            "description": "Echo image/video/document with caption.",
            "examples": [
                "Hello! (Attach image)",
                "This is a test message. (Attach video)",
            ],
        },
    ],
    "note": "Echoes the message.",
}


def handle_function(message: Message):
    if message.media_path:
        message.arguments.append("")
    try:
        if len(message.arguments) == 1:
            raise SystemExit
        parsed = parser(message.arguments[1:])

    except SystemExit:
        raise SendHelp

    if parsed.message:
        message.outgoing_text_message = message.incoming_text_message.lstrip(pluginInfo["command_name"]).strip()
        if message.media_path:
            message.media = {"file": (message.media_mime_type.replace("/", "."), get(appSettings.whatsapp_client_url + message.media_path).content)}
            message.send_file(caption=True)
        else:
            message.send_message()


def parser(args: str) -> ArgumentParser:
    parser = ArgumentParser(description="Echoes the message.")
    parser.add_argument("message", type=str, nargs="*", help="Message to echo.")
    return parser.parse_args(args)
