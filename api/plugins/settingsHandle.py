from api.whatsapp_api_handle import Message
from api.appSettings import appSettings
from argparse import ArgumentParser

pluginInfo = {
    "command_name": "settings",
    "admin_privilege": True,
    "description": "Change and view settings.",
    "internal": False,
}


def handle_function(message: Message):
    try:
        settingArgs = parser(message.arguments[1:])
    except SystemExit:
        pretext = appSettings.admin_command_prefix + " " if pluginInfo["admin_privilege"] else ""
        message.outgoing_text_message = f"""*Usage:*
Change settings:
`/{pretext}settings -c [setting] [value]`
View settings:
`/{pretext}settings -g [setting]`
View all settings:
`/{pretext}settings -g all`

*Available settings:*
- {'\n- '.join(appSettings.list())}"""
        message.send_message()
        return
    if settingArgs.change:
        appSettings.update(settingArgs.change[0], settingArgs.change[1])
        message.outgoing_text_message = f"Setting `{settingArgs.change[0]}` changed to `{settingArgs.change[1]}`."
    elif settingArgs.get:
        if settingArgs.get == "all":
            message.outgoing_text_message = "\n".join([f"- *{setting}*: {getattr(appSettings, setting)}" for setting in appSettings.list()])
        else:
            message.outgoing_text_message = f"*{settingArgs.get}*: {getattr(appSettings, settingArgs.get)}"
    else:
        message.outgoing_text_message = "Invalid arguments."
    message.send_message()


def parser(args: str) -> ArgumentParser:
    parser = ArgumentParser(description="change and view settings.")
    parser.add_argument("-c", "--change", type=str, nargs=2, help="Change settings")
    parser.add_argument("-g", "--get", type=str, choices=appSettings.list().append("all"), help="View settings.")
    return parser.parse_args(args)
