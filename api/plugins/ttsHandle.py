from base64 import b64decode
from argparse import ArgumentParser

from openai import OpenAI, NotFoundError

from api.appSettings import appSettings
from api.whatsapp_api_handle import Message

pluginInfo = {
    "command_name": "tts",
    "admin_privilege": False,
    "description": "Text to speech.",
    "internal": False,
}

# voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
# sendMessage(phone, endpoint="send/file", files={"file": ttsResponse(args.prompt, args.voice if args.voice else "alloy")})
# ffmpeg -i input.oga -acodec mp3 output.mp3


def handle_function(message: Message):
    try:
        if len(message.arguments) == 1:
            raise SystemExit
        parsed = parser(message.arguments[1:])

    except SystemExit:
        pretext = message.command_prefix + (appSettings.admin_command_prefix + " " if pluginInfo["admin_privilege"] else "") + pluginInfo["command_name"]
        message.outgoing_text_message = f"""*Usage:*
- Text to speech: `{pretext} [text]`
- Text to speech using a specific voice: `{pretext} -v [voice] [text]`
- Text to speech using a specific model: `{pretext} -m [model] [text]`"""
        message.send_message()
        return

    if parsed.text:
        try:
            message.media = (f"{'_'.join(parsed.text.split(' ')[:3])}.mp3", ttsResponse(" ".join(parsed.text), parsed.model), "audio/mpeg")
            message.send_audio()
        except NotFoundError:
            message.outgoing_text_message = "Model not found."
            message.send_message()


def parser(args: str) -> ArgumentParser:
    parser = ArgumentParser(description="Text to speech.")
    parser.add_argument("-m", "--model", type=str, default="tts-1", help="Model used for text to speech.")
    parser.add_argument("-v", "--voice", type=str, default="alloy", help="Voice used for text to speech.")
    parser.add_argument("text", type=str, nargs="+", help="Text to speech.")
    return parser.parse_args(args)


def ttsResponse(prompt, voice="alloy", model="tts-1"):
    response = OpenAI(api_key=appSettings.get("openai_api_key")).audio.speech.create(
        model=model,
        voice=voice,
        input=prompt,
        response_format="mp3",
    )
    return response.content
