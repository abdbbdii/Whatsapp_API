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
        settingArgs = parser(message.arguments)
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
- {'\n- '.join([attr for attr in dir(appSettings) if not callable(getattr(appSettings, attr)) and not attr.startswith('__')])}"""
        message.send_message()
        message.outgoing_text_message = str([attr for attr in dir(appSettings) if not callable(getattr(appSettings, attr)) and not attr.startswith("__")] + ["all"])
        message.send_message()
        return
    if settingArgs.change:
        appSettings.update(settingArgs.change[0], settingArgs.change[1])
        message.outgoing_text_message = f"Setting `{settingArgs.change[0]}` changed to `{settingArgs.change[1]}`."
    elif settingArgs.get:
        if settingArgs.get == "all":
            message.outgoing_text_message = "\n".join([f"{attr}: {getattr(appSettings, attr)}" for attr in dir(appSettings) if not callable(getattr(appSettings, attr)) and not attr.startswith("__")])
        else:
            message.outgoing_text_message = f"{settingArgs.get}: {getattr(appSettings, settingArgs.get)}"
    else:
        message.outgoing_text_message = "Invalid arguments."
    message.send_message()


def parser(args: str) -> ArgumentParser:
    parser = ArgumentParser(description="change and view settings.")
    parser.add_argument("-c", "--change", type=str, nargs=2, help="Change settings")
    parser.add_argument("-g", "--get", type=str, choices=[attr for attr in dir(appSettings) if not callable(getattr(appSettings, attr)) and not attr.startswith("__")] + ["all"], help="View settings.")
    return parser.parse_args(args)
