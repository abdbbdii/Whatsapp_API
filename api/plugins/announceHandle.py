import json
from argparse import ArgumentParser

from api.whatsapp_api_handle import Message, SendHelp
from api.models import Users

pluginInfo = {
    "command_name": "announce",
    "admin_privilege": True,
    "description": "Announce a message to all users. (Needs testing.)",
    "internal": False,
}

helpMessage = {
    "commands": [
        {
            "command": "-g [group_name] -m [message]",
            "description": "Announce a message to a specific group.",
            "examples": [
                "-g signedup -m Hello, world!",
                "--group all --message Hello, world!",
            ],
        },
        {
            "command": "-l",
            "description": "List all groups.",
            "examples": [
                "-l",
                "--list",
            ],
        },
    ],
    "note": "Groups are created by admins. Group name 'all' is reserved for all users.",
}


def handle_function(message: Message):
    try:
        if len(message.arguments) == 1:
            raise SystemExit
        parsed = parser(message.arguments[1:])

    except SystemExit:
        raise SendHelp

    users = Users.objects.all()

    if parsed.list:
        group_names = {json.loads(user.description).get("group_name") for user in users if user.description}
        message.outgoing_text_message = f"*Groups:*\n- {'\n- '.join(group_names)}"
        message.send_message()

    if parsed.group and parsed.message:
        message.outgoing_text_message = parsed.message
        for user in users:
            description = json.loads(user.description)
            if description.get("group_name") == parsed.group or parsed.group == "all":
                message.send_to.append(user.user_id) if user.user_id not in message.send_to else None
        message.send_message()

    if (not parsed.group and not parsed.message) or (parsed.group and not parsed.message) or (not parsed.group and parsed.message):
        raise SendHelp


def parser(args: str) -> ArgumentParser:
    parser = ArgumentParser(description="Add or remove an admin.")
    parser.add_argument("-g", "--group", type=str, help="Group name.")
    parser.add_argument("-l", "--list", action="store_true", help="List all groups.")
    parser.add_argument("-m", "--message", type=str, nargs="+", help="Message to announce.")
    return parser.parse_args(args)
