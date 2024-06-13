from argparse import ArgumentParser

from openai import OpenAI, NotFoundError

from api.appSettings import appSettings
from api.whatsapp_api_handle import Message

pluginInfo = {
    "command_name": "gpt",
    "admin_privilege": False,
    "description": "Chat with the AI.",
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
- Chat with the AI: `{pretext} [message]`
- Chat with the AI using a specific model: `{pretext} -m [model] [message]`"""
        message.send_message()
        return

    if parsed.prompt:
        try:
            message.outgoing_text_message = gptResponse(" ".join(parsed.prompt), parsed.model)
        except NotFoundError:
            message.outgoing_text_message = "Model not found."
        message.send_message()


def gptResponse(prompt, model):
    response = OpenAI(api_key=appSettings.openai_api_key).chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a question answering bot. Be as precise as possible. And respond to the user's question. If you don't know the answer, just say cant answer.",
            },
            {"role": "user", "content": "Here are some questions:\n\n" + prompt},
        ],
    )
    return response.choices[0].message.content


def parser(args: str) -> ArgumentParser:
    parser = ArgumentParser(description="Chat with the AI.")
    parser.add_argument("-m", "--model", type=str, default="gpt-3.5-turbo", help="Model to chat with the AI.")
    parser.add_argument("prompt", type=str, nargs="+", help="Prompt to chat with the AI.")
    return parser.parse_args(args)
