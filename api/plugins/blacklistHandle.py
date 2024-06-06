from api.whatsapp_api_handle import Message
from api.appSettings import appSettings
from argparse import ArgumentParser

pluginInfo = {
    "command_name": "blacklist",
    "admin_privilege": True,
    "description": "Add or remove a number from blacklist.",
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
- Add member(s) to blacklist:
`/{pretext+pluginInfo["command_name"]} -a [number] [number]...`
- Remove member(s) from blacklist:
`/{pretext+pluginInfo["command_name"]} -r [number] [number]...`
- Get blacklist:
`/{pretext+pluginInfo["command_name"]} -g`
"""
        message.send_message()
        return

    if parsed.add:
        for number in parsed.add:
            appSettings.append("blacklist_ids", number)
        message.outgoing_text_message = f"*Blacklisted*: {', '.join(parsed.add)}."

    if parsed.remove:
        for number in parsed.remove:
            appSettings.remove("blacklist_ids", number)
        message.outgoing_text_message = f"*Removed from blacklist*: {', '.join(parsed.remove)}."

    if parsed.get:
        message.outgoing_text_message = "*Blacklisted*: " + ", ".join(appSettings.blacklist_ids)

    message.send_message()


def parser(args: str) -> ArgumentParser:
    parser = ArgumentParser(description="Add or remove a number from blacklist.")
    parser.add_argument("-a", "--add", nargs="+", help="Add member(s) to blacklist.")
    parser.add_argument("-r", "--remove", type=str, nargs="+", choices=appSettings.blacklist_ids, help="Remove member(s) from blacklist.")
    parser.add_argument("-g", "--get", action="store_true", help="Get blacklist.")
    return parser.parse_args(args)
