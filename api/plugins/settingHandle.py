from api.whatsapp_api_handle import Message
from api.appSettings import appSettings
from argparse import ArgumentParser

pluginInfo = {
    "command_name": "setting",
    "admin_privilege": True,
    "description": "Change and view settings.",
    "internal": False,
}


def handle_function(message: Message):
    try:
        if len(message.arguments) == 1:
            raise SystemExit
        parsed = parser(message.arguments[1:])

    except SystemExit:
        pretext = appSettings.admin_command_prefix + " " if pluginInfo["admin_privilege"] else ""
        message.outgoing_text_message = f"""*Usage:*
- Change setting: `/{pretext+pluginInfo["command_name"]} -c [setting] [value]`
- View setting: `/{pretext+pluginInfo["command_name"]} -g [setting]`
- View all settings: `/{pretext+pluginInfo["command_name"]} -g all`

*Available settings:*
- {'\n- '.join(appSettings.list())}"""
        message.send_message()
        return

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
