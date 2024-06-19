import re

from api.models import Kharchey
from api.whatsapp_api_handle import Message
from api.appSettings import appSettings

pluginInfo = {
    "command_name": "kharchey",
    "description": "Count spent money",
    "admin_privilege": False,
    "internal": True,
}


def preprocess(message: Message) -> None:
    if message.group == appSettings.kharchey_group_id and message.incoming_text_message and not bool(re.match(r"\.[^\.].*", message.incoming_text_message)):
        message.incoming_text_message = "./kharchey " + message.incoming_text_message


def handle_function(message: Message):
    def parse_item(text: str) -> dict[str, str]:
        if match := re.match(r"(\d+)(?:x(\d+))?\s+(.+)", text):
            price = int(match.group(1))
            quantity = int(match.group(2)) if match.group(2) else 1
            item = match.group(3)
            if match.group(2):
                price, quantity = quantity, price
            return {
                "price": price,
                "quantity": quantity,
                "item": item,
            }
        return {}

    def get_list(withtime: bool = False, all=False) -> str:
        total = 0
        outgoing_text_message = ""
        items = Kharchey.objects.filter(group=message.group, sender=message.sender).order_by("date") if not all else Kharchey.objects.filter(group=message.group).order_by("date")
        for i, item in enumerate(items):
            time = f"`{item.date.day:02d}/{item.date.month:02d}/{item.date.year:04d} {((item.date.hour - 12) if item.date.hour > 12 else item.date.hour):02d}:{item.date.minute:02d} {"PM" if item.date.hour > 12 else "AM"}` " if withtime else ""
            outgoing_text_message += f"{i+1}. {time}`Rs. {str(item.quantity)+'x'+str(item.price)+'='+str(item.quantity*item.price) if item.quantity > 1 else str(item.price)}` for {item.item}\n"
            total += item.quantity * item.price
        if total:
            outgoing_text_message += f"\n*Total: {total}*"
        else:
            outgoing_text_message = ""
        return outgoing_text_message

    if message.arguments[1].casefold() == "Help".casefold():
        message.outgoing_text_message = """*💵 Help 💵*
- `[quantity]x[price] [item]`: Add items with quantity
- `[price] [item]`: Add items without quantity
- `List`: Get list of items
- `List withtime`: Get list of items with time
- `List all`: Get list of all participants
- `Edit [item#] [quantity]x[price] [item]`: Edit specific item in list
- `Edit [item#] [price] [item]`: Edit specific item in list
- `Clear`: Clear all items from list
- `Clear [item1#] [item2#] ...`: Clear specific items from list
- `Help`: Show this message

_Note: Only the person who added the item can clear it._"""
        message.send_message()

    elif message.arguments[1].casefold() == "List".casefold():
        message.outgoing_text_message = "*💵 List 💵*\n"
        if lis := get_list(len(message.arguments) == 3 and message.arguments[2] == "withtime"):
            message.outgoing_text_message += lis
        elif lis := get_list(len(message.arguments) == 3 and message.arguments[2] == "all", all=True):
            message.outgoing_text_message += lis
        else:
            message.outgoing_text_message = "No items in list"
        message.send_message()

    elif message.arguments[1].casefold() == "Edit".casefold():
        if len(message.arguments) > 4 and message.arguments[2].isdigit():
            item_no = int(message.arguments[2])
            items = Kharchey.objects.filter(group=message.group, sender=message.sender).order_by("date")
            if item_no <= len(items):
                item = items[item_no - 1]
                if parsed := parse_item(" ".join(message.arguments[3:])):
                    item.item = parsed["item"]
                    item.quantity = parsed["quantity"]
                    item.price = parsed["price"]
                    item.save()
                    message.outgoing_text_message = f"Item {item_no}. *{item.item}* updated\n"
                else:
                    message.outgoing_text_message = f"Item {item_no}. *{item.item}* not updated\n"
            else:
                message.outgoing_text_message = f"Item {item_no} not found\n"
        else:
            message.outgoing_text_message = "Usage: `Edit [item#] [quantity]x[price] [item]` or `Edit [item#] [price] [item]`"
        message.send_message()

    elif message.arguments[1].casefold() == "Clear".casefold():
        if len(message.arguments) > 2:
            items_in_list = Kharchey.objects.filter(group=message.group, sender=message.sender).order_by("date")
            for item_no in message.arguments[2:]:
                if item_no.isdigit() and int(item_no) <= len(items_in_list):
                    item = items_in_list[int(item_no) - 1]
                    item.delete()
                    message.outgoing_text_message += f"Item {item_no}. *{item.item}* cleared\n"
                else:
                    message.outgoing_text_message += f"Item {item_no} not found\n"
        elif len(message.arguments) == 2:
            Kharchey.objects.filter(group=message.group, sender=message.sender).delete()
            message.outgoing_text_message = "All items cleared"
        else:
            message.outgoing_text_message = "Usage: `Clear [item1#] [item2#] ...`"
        message.send_message()

    elif parse_item(message.incoming_text_message.lstrip("kharchey").strip().split("\n")[0]):
        message_items = message.incoming_text_message.lstrip("kharchey").strip().split("\n")
        success = []
        failed = []
        for message_item in message_items:
            if parsed := parse_item(message_item):
                Kharchey.objects.create(
                    item=parsed["item"],
                    quantity=parsed["quantity"],
                    price=parsed["price"],
                    group=message.group,
                    sender=message.sender,
                ).save()
                success.append(parsed["item"])
            else:
                failed.append(message_item)
        if success:
            message.outgoing_text_message += f"Added *{', '.join(success)}* to list\n"
        if failed:
            message.outgoing_text_message += f"Failed to add *{', '.join(failed)}* to list\n"
            message.outgoing_text_message += "Usage: `[quantity]x[price] [item]`"
        if message.outgoing_text_message:
            message.outgoing_text_message += "\n*💵 List 💵*\n"
            lis = get_list(False)
            message.outgoing_text_message += lis if lis else "No items in list"
            message.send_message()
