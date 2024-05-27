from api.whatsapp_api_handle import appSettings, Message
from argparse import ArgumentParser
import shlex

pluginInfo = {
    "command_name": "admin",
    "admin_privilege": True,
    "description": "Admin commands to manage admin list. Use `/abd admin help` to see available commands.",
    "internal": False,
}


def handle_function(message: Message):
    adminArgs = parser(" ".join(message.arguments), appSettings["adminIds"])
    if isinstance(adminArgs, str):
        message.outgoing_text_message = adminArgs
    elif adminArgs.add:
        appSettings["adminIds"] += adminArgs.add
        message.outgoing_text_message = f"Admin(s) `{adminArgs.add}` successfully added to the adminlist."
    elif adminArgs.remove:
        for number in adminArgs.remove:
            appSettings["adminIds"].remove(number)
        message.outgoing_text_message = f"Admin(s) `{adminArgs.remove}` successfully removed from the adminlist."
    elif adminArgs.get:
        message.outgoing_text_message = f"{appSettings['adminIds']}"
    # setAppSettings()
    message.send_message()


def parser(input: str, adminlist: list):
    parser = ArgumentParser(description="Add or remove an admin.")
    parser.add_argument("-a", "--add", nargs="+", help="Add number(s) (92xxxxxxxxxx) to adminlist.")
    parser.add_argument("-r", "--remove", type=str, nargs="+", choices=adminlist, help="Remove number(s) (92xxxxxxxxxx) from adminlist.")
    parser.add_argument("-g", "--get", action="store_true", help="View all admins.")
    try:
        args = parser.parse_args(shlex.split(input))
    except SystemExit:
        return parser.format_help()
    return args
