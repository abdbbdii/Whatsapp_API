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
        parsed = parser(message.arguments[1:])

    except SystemExit:
        pretext = appSettings.admin_command_prefix + " " if pluginInfo["admin_privilege"] else ""
        message.outgoing_text_message = f"""*Usage:*
- Add admin(s):
`/{pretext}admin -a [number]`
- Remove admin(s):
`/{pretext}admin -r [number]`
- Get admin list:
`/{pretext}admin -g`
"""
        message.send_message()
        return

    if parsed.add:
        for number in parsed.add:
            appSettings.append("admin_ids", number)
        message.outgoing_text_message = f"Admin(s) added: {', '.join(parsed.add)}."

    elif parsed.remove:
        for number in parsed.remove:
            appSettings.remove("admin_ids", number)
        message.outgoing_text_message = f"Admin(s) removed: {', '.join(parsed.remove)}."

    elif parsed.get:
        message.outgoing_text_message = "Admins: " + ", ".join(appSettings.admin_ids)

    message.send_message()


def parser(args: str) -> ArgumentParser:
    parser = ArgumentParser(description="Add or remove an admin.")
    parser.add_argument("-a", "--add", nargs="+", help="Add admin(s).")
    parser.add_argument("-r", "--remove", type=str, nargs="+", choices=appSettings.admin_ids, help="Remove admin(s).")
    parser.add_argument("-g", "--get", action="store_true", default=True, help="Get admin list.")
    return parser.parse_args(args)
