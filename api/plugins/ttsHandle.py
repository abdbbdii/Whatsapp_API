from argparse import ArgumentParser

from openai import OpenAI, NotFoundError

from api.appSettings import appSettings
from api.whatsapp_api_handle import Message, SendHelp

pluginInfo = {
    "command_name": "tts",
    "admin_privilege": False,
    "description": "Text to speech.",
    "internal": False,
}

# sendMessage(phone, endpoint="send/file", files={"file": ttsResponse(args.prompt, args.voice if args.voice else "alloy")})
# ffmpeg -i input.oga -acodec mp3 output.mp3

helpMessage = {
    "commands": [
        {
            "command": "[text]",
            "description": "Text to speech.",
            "examples": [
                "Hello!",
                "This is a test message.",
            ],
        },
        {
            "command": "-v [voice] [text]",
            "description": "Text to speech using a specific voice.",
            "examples": [
                "-v alloy Hello!",
                "-v echo This is a test message.",
            ],
        },
        {
            "command": "-m [model] [text]",
            "description": "Text to speech using a specific model.",
            "examples": [
                "-m tts-1 Hello!",
                "-m tts-1-hd This is a test message.",
            ],
        },
    ],
    "note": "Available voices: alloy, echo, fable, onyx, nova, shimmer. Available models: tts-1, tts-1-hd.",
}

def handle_function(message: Message):
    try:
        if len(message.arguments) == 1:
            raise SystemExit
        parsed = parser(message.arguments[1:])

    except SystemExit:
        raise SendHelp

    if parsed.text:
        try:
            message.media = {"file": (f"{'_'.join(parsed.text[:3])}.mp3", ttsResponse(" ".join(parsed.text), parsed.voice, parsed.model), "audio/mpeg")}
            message.send_file()
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
    response = OpenAI(api_key=appSettings.openai_api_key).audio.speech.create(
        model=model,
        voice=voice,
        input=prompt,
        response_format="mp3",
    )
    return response.content
