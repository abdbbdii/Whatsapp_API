from base64 import b64decode
from argparse import ArgumentParser

from openai import OpenAI, NotFoundError

from api.appSettings import appSettings
from api.whatsapp_api_handle import Message

pluginInfo = {
    "command_name": "img",
    "admin_privilege": False,
    "description": "Generate image (Not working at the moment).",
    "internal": False,
}


def handle_function(message: Message):
    try:
        if len(message.arguments) == 1:
            raise SystemExit
        parsed = parser(message.arguments[1:])

    except SystemExit:
        pretext = message.command_prefix + (appSettings.admin_command_prefix + " " if pluginInfo["admin_privilege"] else "") + pluginInfo["command_name"]
        message.outgoing_text_message = f"""*Usage:*
- Generate Image: `{pretext} [description]`
- Generate Image using a specific model: `{pretext} -m [model] [description]`"""
        message.send_message()
        return

    if parsed.description:
        try:
            message.media = {"file": (f"{'_'.join(parsed.description[:3])}.jpg", imgResponse(" ".join(parsed.description), parsed.model), "image/jpeg")}
            message.send_file()  # FIXME: cant send image
        except NotFoundError:
            message.outgoing_text_message = "Model not found."
            message.send_message()


def parser(args: str) -> ArgumentParser:
    parser = ArgumentParser(description="Generate image.")
    parser.add_argument("-m", "--model", type=str, default="dall-e-2", help="Model to generate image.")
    parser.add_argument("description", type=str, nargs="+", help="Description to generate image.")
    return parser.parse_args(args)


def imgResponse(prompt, model="dall-e-2"):
    response = OpenAI(api_key=appSettings.openai_api_key).images.generate(
        model=model,
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        response_format="b64_json",
        n=1,
    )
    return b64decode(response.data[0].b64_json)
