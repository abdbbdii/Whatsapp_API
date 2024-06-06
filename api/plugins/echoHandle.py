from api.whatsapp_api_handle import Message
from api.appSettings import appSettings
from argparse import ArgumentParser
from requests import get

pluginInfo = {
    "command_name": "echo",
    "admin_privilege": False,
    "description": "Echoes the message.",
    "internal": False,
}


def handle_function(message: Message):
    if message.media_path:
        message.arguments.append("")
    try:
        if len(message.arguments) == 1:
            raise SystemExit
        parsed = parser(message.arguments[1:])

    except SystemExit:
        pretext = appSettings.admin_command_prefix + " " if pluginInfo["admin_privilege"] else ""
        message.outgoing_text_message = f"""*Usage:*
- Echo message:
`/{pretext+pluginInfo["command_name"]} [message]`
- Echo image with caption:
Attach image with caption: `/{pretext+pluginInfo["command_name"]} [caption]`
- Echo image without caption:
Attach image with caption: `/{pretext+pluginInfo["command_name"]}`"""
        message.send_message()
        return

    if parsed.message:
        message.outgoing_text_message = " ".join(parsed.message)

    else:
        message.outgoing_text_message = "Invalid arguments."

    if message.media_path:
        # TODO
        message.media = {"file": (message.media_mime_type.replace("/", "."), get(appSettings.whatsapp_client_url + message.media_path).content)}
        message.send_file(caption=True)
    else:
        message.send_message()


def parser(args: str) -> ArgumentParser:
    parser = ArgumentParser(description="Echoes the message.")
    parser.add_argument("message", type=str, nargs="*", help="Message to echo.")
    return parser.parse_args(args)
