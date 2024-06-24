from api.whatsapp_api_handle import Message, SendHelp
from api.appSettings import appSettings
from argparse import ArgumentParser

pluginInfo = {
    "command_name": "setting",
    "admin_privilege": True,
    "description": "Change and view settings.",
    "internal": False,
}

helpMessage = {
    "commands": [
        {
            "command": "-c [setting] [value]",
            "description": "Change setting.",
            "examples": [
                "-c admin_command_prefix !",
                "--change admin_command_prefix !",
            ],
        },
        {
            "command": "-g [setting]",
            "description": "View setting.",
            "examples": [
                "-g admin_command_prefix",
                "--get admin_command_prefix",
            ],
        },
        {
            "command": "-g all",
            "description": "View all settings.",
            "examples": [
                "-g all",
                "--get all",
            ],
        },
    ],
    "note": f"Available settings:\n- {'\n- '.join(appSettings.list())}",
}

def handle_function(message: Message):
    try:
        if len(message.arguments) == 1:
            raise SystemExit
        parsed = parser(message.arguments[1:])

    except SystemExit:
        raise SendHelp

    if parsed.change:
        appSettings.update(parsed.change[0], parsed.change[1])
        message.outgoing_text_message = f"Setting `{parsed.change[0]}` changed to `{parsed.change[1]}`."
        message.send_message()

    if parsed.get:
        if parsed.get == "all":
            message.outgoing_text_message = "\n".join([f"- *{setting}*: {getattr(appSettings, setting)}" for setting in appSettings.list()])
        elif hasattr(appSettings, parsed.get):
            message.outgoing_text_message = f"*{parsed.get}*: {getattr(appSettings, parsed.get)}"
        else:
            message.outgoing_text_message = f"Setting `{parsed.get}` not found."
        message.send_message()


def parser(args: str) -> ArgumentParser:
    parser = ArgumentParser(description="change and view settings.")
    parser.add_argument("-c", "--change", type=str, nargs=2, help="Change settings")
    parser.add_argument("-g", "--get", type=str, help="View settings.")
    return parser.parse_args(args)
