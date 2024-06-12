from api.whatsapp_api_handle import Message
import re
from api.models import Kharchey

pluginInfo = {
    "command_name": "kharchey",
    "description": "Count spent money",
    "admin_privilege": False,
    "internal": True,
}


def handle_function(message: Message):

    def get_list() -> str:
        total = 0
        outgoing_text_message = ""
        for i, item in enumerate(Kharchey.objects.filter(group=message.group, sender=message.sender).order_by("date")):
            time = f"{item.date.day}/{item.date.month}/{item.date.year} {item.date.hour%12 if item.date.hour%12 != 0 else 12}:{item.date.minute} {'AM' if item.date.hour < 12 else 'PM'}"
            outgoing_text_message += f"{i+1}. `{time}` {item.item} {str(item.quantity)+'x' if item.quantity != 1 else ""}{item.price} = {item.quantity * item.price}\n"
            total += item.quantity * item.price
        if total:
            outgoing_text_message += f"\n*Total: {total}*"
        else:
            outgoing_text_message = "List is empty"
        return outgoing_text_message

    if message.arguments[1] == "List" or message.arguments[1] == "list":
        message.outgoing_text_message = "*💵 List 💵*\n"
        message.outgoing_text_message += get_list()
        message.send_message()

    elif message.arguments[1] == "Help" or message.arguments[1] == "help":
        message.outgoing_text_message = """*💵 Help 💵*
- `List`: Get list of items
- `Clear`: Clear all items from list
- `Clear [item#1] [item#2] ...`: Clear specific item from list
- `[quantity]x[price] [item]`: Add items with quantity
- `[price] [item]`: Add items without quantity
- `Help`: Show this message

_Note: Only the person who added the item can clear it._"""
        message.send_message()

    elif message.arguments[1] == "Clear" or message.arguments[1] == "clear":
        if len(message.arguments) > 2:
            message.outgoing_text_message = ""
            items_in_list = len(Kharchey.objects.filter(group=message.group, sender=message.sender).order_by("date"))
            for item_no in message.arguments[2:]:
                if item_no.isdigit() and int(item_no) <= items_in_list:
                    item = Kharchey.objects.filter(group=message.group, sender=message.sender)[int(item_no) - 1]
                    item.delete()
                    message.outgoing_text_message += f"Item {item_no} ({item.item}) cleared\n"
                else:
                    message.outgoing_text_message += f"Item {item_no} not found\n"
        else:
            Kharchey.objects.filter(group=message.group, sender=message.sender).delete()
            message.outgoing_text_message = "All items cleared"

        message.send_message()

    else:
        message_items = message.incoming_text_message.lstrip("kharchey").strip().split("\n")

        for message_item in message_items:
            if match := re.match(r"(\d+)(?:x(\d+))?\s+(.+)", message_item):
                price = int(match.group(1))
                quantity = int(match.group(2)) if match.group(2) else 1
                item = match.group(3)

                if match.group(2):
                    price, quantity = quantity, price

                instance = {
                    "price": price,
                    "quantity": quantity,
                    "item": item,
                }

                Kharchey.objects.create(
                    item=instance["item"],
                    quantity=instance["quantity"],
                    price=instance["price"],
                    group=message.group,
                    sender=message.sender,
                ).save()

                message.outgoing_text_message += f"Added *{instance['item']}* to list\n"

        if message.outgoing_text_message:
            message.outgoing_text_message += "\n*💵 List 💵*\n"
            message.outgoing_text_message += get_list()
            message.send_message()
