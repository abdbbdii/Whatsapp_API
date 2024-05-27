from api.whatsapp_api_handle import appSettings, Message
from argparse import ArgumentParser
import shlex

pluginInfo = {
    "command_name": "blacklist",
    "admin_privilege": True,
    "description": "Blacklist commands to manage blacklist. Use ```/abd blacklist help``` to see available commands.",
    "internal": False,
}


def handle_function(message: Message):
    blacklistArgs = parser.blackListParser(" ".join(message.arguments), appSettings["blacklist"])
    if isinstance(blacklistArgs, str):
        message.outgoing_text_message = blacklistArgs
    elif blacklistArgs.add:
        appSettings["blacklist"] += blacklistArgs.add
        message.outgoing_text_message = f"Number(s) ```{blacklistArgs.add}``` successfully added to the blackList."
    elif blacklistArgs.remove:
        for number in blacklistArgs.remove:
            appSettings["blacklist"].remove(number)
        message.outgoing_text_message = f"Number(s) ```{blacklistArgs.remove}``` successfully removed from the blackList."
    elif blacklistArgs.get:
        message.outgoing_text_message = f"{appSettings['blacklist']}"
    # setAppSettings()
    message.send_message()


def parser(input: str, blacklist: list):
    parser = ArgumentParser(description="Allow list to add or remove from the automatic conversation.")
    parser.add_argument("-a", "--add", type=str, nargs="+", help="Add number(s) (92xxxxxxxxxx) to blacklist.")
    parser.add_argument("-r", "--remove", type=str, nargs="+", choices=blacklist, help="Remove number(s) (92xxxxxxxxxx) from blacklist.")
    parser.add_argument("-g", "--get", action="store_true", help="View all blocked numbers.")
    try:
        args = parser.parse_args(shlex.split(input))
    except SystemExit:
        return parser.format_help()
    return args
