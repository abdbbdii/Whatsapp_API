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
    settingArgs = parser(message.arguments)
    if isinstance(settingArgs, str):
        message.outgoing_text_message = '\n> '.join(settingArgs.split('\n'))
    elif settingArgs.change:
        appSettings.update(settingArgs.change[0], settingArgs.change[1])
        message.outgoing_text_message = f"Setting `{settingArgs.change[0]}` changed to `{settingArgs.change[1]}`."
    elif settingArgs.get:
        if settingArgs.get == "all":
            message.outgoing_text_message = "\n".join([f"{attr}: {getattr(appSettings, attr)}" for attr in dir(appSettings) if not callable(getattr(appSettings, attr)) and not attr.startswith('__')])
        else:
            message.outgoing_text_message = f"{settingArgs.get}: {getattr(appSettings, settingArgs.get)}"
    else:
        message.outgoing_text_message = "Invalid arguments."
    message.send_message()


def parser(args: str):
    parser = ArgumentParser(description="change and view settings.")
    parser.add_argument("-c", "--change", type=str, nargs=2, help="Change settings")
    parser.add_argument("-g", "--get", type=str, choices=[attr for attr in dir(appSettings) if not callable(getattr(appSettings, attr)) and not attr.startswith('__')] + ["all"], help="View settings.")
    try:
        parse = parser.parse_args(args)
    except SystemExit:
        return parser.format_help()
    return parse
