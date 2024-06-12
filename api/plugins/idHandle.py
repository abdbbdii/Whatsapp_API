from api.whatsapp_api_handle import Message

pluginInfo = {
    "command_name": "id",
    "admin_privilege": False,
    "description": "Find out the ID of a user or a group.",
    "internal": False,
}


def handle_function(message: Message):
    message.outgoing_text_message = f"""*IDs*
- *Message ID*: {message.incoming_message_id}
- *Sender ID*: {message.sender}
{f"- *Group ID*: {message.group}" if message.group else ""}"""
    message.send_message()