from api.whatsapp_api_handle import Message
from api.appSettings import appSettings
from openai import OpenAI
import requests

pluginInfo = {
    "command_name": "solve",
    "admin_privilege": False,
    "description": "Solve the simple and multiple-choice questions in the image.",
    "internal": False,
}


def handle_function(message: Message):
    if not message.media_path:
        message.outgoing_text_message = f"""*Usage:*
- Send an image caption: `{message.command_prefix+pluginInfo['command_name']}`"""
        message.send_message()
        return

    response = requests.post(
        "https://api.ocr.space/parse/image",
        files={
            "image": requests.get(appSettings.whatsapp_client_url + message.media_path).content,
        },
        data={
            "apikey": appSettings.ocr_space_api_key,
            "filetype": "JPG",
            "OCREngine": 2,
        },
    ).json()
    message.outgoing_text_message = gptResponse(response["ParsedResults"][0]["ParsedText"] if not response["IsErroredOnProcessing"] else response["ErrorMessage"])
    message.send_message()


def gptResponse(prompt):
    response = OpenAI(api_key=appSettings.openai_api_key).chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a question answering bot. Be as precise as possible. And respond to the user's question. If you don't know the answer, just say cant answer.",
            },
            {"role": "user", "content": "Here are some questions:\n\n" + prompt},
        ],
    )
    return response.choices[0].message.content
