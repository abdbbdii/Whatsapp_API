from api.whatsapp_api_handle import Message
from api.appSettings import appSettings
from argparse import ArgumentParser

pluginInfo = {
    "command_name": "blacklist",
    "admin_privilege": True,
    "description": "Add or remove a number from blacklist.",
    "internal": False,
}

helpMessage = {
    "commands": [
        {
            "command": "-a [number] [number] ...",
            "description": "Add members to blacklist.",
            "examples": [
                "-a 923201234567",
                "--add 923123098456 923201234567 923123456789",
            ],
        },
        {
            "command": "-r [number] [number] ...",
            "description": "Remove members from blacklist.",
            "examples": [
                "-r 923201234567",
                "--remove 923123098456 923201234567 923123456789",
            ],
        },
        {
            "command": "-g",
            "description": "Get blacklist.",
            "examples": [
                "-g",
                "--get",
            ],
        },
    ],
    "note": "Blacklisted members cannot use the bot.",
}

def handle_function(message: Message):
    try:
        if len(message.arguments) == 1:
            raise SystemExit
        parsed = parser(message.arguments[1:])

    except SystemExit:
        pretext = message.command_prefix + (appSettings.admin_command_prefix + " " if pluginInfo["admin_privilege"] else "") + pluginInfo["command_name"]
        message.outgoing_text_message = f"""*Usage:*
- Add members to blacklist: `{pretext} -a [number] [number]...`
- Remove members from blacklist: `{pretext} -r [number] [number]...`
- Get blacklist: `{pretext} -g`"""
        message.send_message()
        return

    if parsed.add:
        success = []
        fail = []
        for number in parsed.add:
            if number not in appSettings.blacklist_ids:
                appSettings.append("blacklist_ids", number)
                success.append(number)
            else:
                fail.append(number)
        if success:
            message.outgoing_text_message = f"*Added to blacklist*: {', '.join(success)}."
            message.send_message()
        if fail:
            message.outgoing_text_message = f"*Already in blacklist*: {', '.join(fail)}."
            message.send_message()

    if parsed.remove:
        success = []
        fail = []
        for number in parsed.remove:
            if number in appSettings.blacklist_ids:
                appSettings.remove("blacklist_ids", number)
                success.append(number)
            else:
                fail.append(number)
        if success:
            message.outgoing_text_message = f"*Removed from blacklist*: {', '.join(success)}."
            message.send_message()
        if fail:
            message.outgoing_text_message = f"*Not in blacklist*: {', '.join(fail)}."
            message.send_message()

    if parsed.get:
        message.outgoing_text_message = "*Blacklisted*: " + ", ".join(appSettings.blacklist_ids)
        message.send_message()


def parser(args: str) -> ArgumentParser:
    parser = ArgumentParser(description="Add or remove a number from blacklist.")
    parser.add_argument("-a", "--add", nargs="+", help="Add members to blacklist.")
    parser.add_argument("-r", "--remove", type=str, nargs="+", help="Remove members from blacklist.")
    parser.add_argument("-g", "--get", action="store_true", help="Get blacklist.")
    return parser.parse_args(args)
