from api.whatsapp_api_handle import Message
from api.appSettings import appSettings
from argparse import ArgumentParser

pluginInfo = {
    "command_name": "admin",
    "admin_privilege": True,
    "description": "Add or remove an admin.",
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
- Add admins: `/{pretext+pluginInfo["command_name"]} -a [number] [number]...`
- Remove admins: `/{pretext+pluginInfo["command_name"]} -r [number] [number]...`
- Get admin list: `/{pretext+pluginInfo["command_name"]} -g`"""
        message.send_message()
        return

    if parsed.add:
        for number in parsed.add:
            appSettings.append("admin_ids", number)
        message.outgoing_text_message = f"*Admins added*: {', '.join(parsed.add)}."
        message.send_message()

    if parsed.remove:
        for number in parsed.remove:
            try:
                appSettings.remove("admin_ids", number)
                message.outgoing_text_message = f"*Admins removed*: {', '.join(parsed.remove)}."
            except ValueError:
                message.outgoing_text_message = f"{number} is not an admin."
        message.send_message()

    if parsed.get:
        message.outgoing_text_message = "*Admins*: " + ", ".join(appSettings.admin_ids)
        message.send_message()


def parser(args: str) -> ArgumentParser:
    parser = ArgumentParser(description="Add or remove an admin.")
    parser.add_argument("-a", "--add", nargs="+", help="Add admins.")
    parser.add_argument("-r", "--remove", type=str, nargs="+", help="Remove admins.")
    parser.add_argument("-g", "--get", action="store_true", help="Get admin list.")
    return parser.parse_args(args)
