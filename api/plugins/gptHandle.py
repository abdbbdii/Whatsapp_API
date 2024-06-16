from argparse import ArgumentParser

from openai import OpenAI, NotFoundError

from api.appSettings import appSettings
from api.whatsapp_api_handle import Message
from api.models import GPTResponse

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
            message.outgoing_text_message = gptResponse(" ".join(parsed.prompt), parsed.model, get_previous_messages(message))
        except NotFoundError:
            message.outgoing_text_message = "Model not found."
        message.send_message()
        save_response(message)


def gptResponse(prompt: str, model: str, previous_messages: list[dict[str, str]] | None = None) -> str:
    response = OpenAI(api_key=appSettings.openai_api_key).chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a whatsapp bot. You are assisting a user in a chat. If they need help or ask a question that you can't answer, tell them to contact owner. Number: +92 312 4996133, Name: abd.",
            },
            *previous_messages,
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return response.choices[0].message.content


def get_previous_messages(message: Message) -> list[dict[str, str]]:
    previous_messages = []
    for response in GPTResponse.objects.filter(group=message.group, sender=message.sender).order_by("-date")[:5]:
        previous_messages.append({"role": "user", "content": response.message})
        previous_messages.append({"role": "assistant", "content": response.response})
    return previous_messages


def save_response(message: Message) -> None:
    GPTResponse.objects.create(message=message.incoming_text_message, response=message.outgoing_text_message, group=message.group, sender=message.sender)


def parser(args: str) -> ArgumentParser:
    parser = ArgumentParser(description="Chat with the AI.")
    parser.add_argument("-m", "--model", type=str, default="gpt-3.5-turbo", help="Model to chat with the AI.")
    parser.add_argument("prompt", type=str, nargs="+", help="Prompt to chat with the AI.")
    return parser.parse_args(args)
