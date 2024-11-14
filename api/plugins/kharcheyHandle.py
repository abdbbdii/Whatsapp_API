import re

from api.models import Kharchey
from api.whatsapp_api_handle import Message, SendHelp
from api.appSettings import appSettings

pluginInfo = {
    "command_name": "kharchey",
    "description": "Count spent money",
    "admin_privilege": False,
    "internal": True,
}

helpMessage = {
    "commands": [
        {
            "command": "[quantity]x[price] [item]",
            "description": "Add items with quantity.",
            "examples": [
                "2x100 Milk",
                "3x50 Chips",
            ],
        },
        {
            "command": "[price] [item]",
            "description": "Add items without quantity.",
            "examples": [
                "100 Milk",
                "50 Chips",
            ],
        },
        {
            "command": "Edit [item#] [quantity]x[price] [item]",
            "description": "Edit specific item in list.",
            "examples": [
                "Edit 1 2x100 Milk",
                "Edit 2 3x50 Chips",
            ],
        },
        {
            "command": "Edit [item#] [price] [item]",
            "description": "Edit specific item in list.",
            "examples": [
                "Edit 1 100 Milk",
                "Edit 2 50 Chips",
            ],
        },
        {
            "command": "Clear [item#] [item#] ...",
            "description": "Clear specific items from list.",
            "examples": [
                "Clear 1 2",
                "Clear 1 2 3",
            ],
        },
        {
            "command": "Clear",
            "description": "Clear all items from list.",
        },
        {
            "command": "List",
            "description": "Get list of items.",
        },
        {
            "command": "List withtime",
            "description": "Get list of items with time.",
        },
        {
            "command": "List all",
            "description": "Get list of all participants.",
        },
        {
            "command": "Help",
            "description": "Show this message.",
        },
    ],
    "note": "Only the person who added the item can edit or clear it.",
}


def preprocess(message: Message) -> None:
    if message.group == appSettings.kharchey_group_id and message.incoming_text_message and not bool(re.match(r"\.[^\.].*", message.incoming_text_message)) and not message.incoming_text_message.startswith("."):
        message.incoming_text_message = "./" + pluginInfo["command_name"] + " " + message.incoming_text_message


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
            time = f"`{item.date.day:02d}/{item.date.month:02d}/{item.date.year:04d} {((item.date.hour - 12) if item.date.hour > 12 else item.date.hour):02d}:{item.date.minute:02d} {'PM' if item.date.hour > 12 else 'AM'}` " if withtime else ""
            outgoing_text_message += f"{i+1}. {time}`{str(item.quantity)+'x'+str(item.price)+'='+str(item.quantity*item.price) if item.quantity > 1 else str(item.price)}` {item.item}\n"
            total += item.quantity * item.price
        if total:
            outgoing_text_message += f"\n*Total: {total}*"
        else:
            outgoing_text_message = ""
        return outgoing_text_message

    def send_list(withtime: bool = False, all: bool = False) -> None:
        message.outgoing_text_message += "*List*\n"
        lis = get_list(withtime, all)
        message.outgoing_text_message += lis if lis else "No items in list"
        message.send_message()

    if message.arguments[1].casefold() == "Help".casefold():
        raise SendHelp

    elif message.arguments[1].casefold() == "List".casefold():

        if "withtime" in message.arguments:
            send_list(withtime=True)
        elif "all" in message.arguments:
            send_list(all=True)
        elif "withtime" in message.arguments and "all" in message.arguments:
            send_list(withtime=True, all=True)
        else:
            send_list()

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
        else:
            message.outgoing_text_message = "Usage: `Edit [item#] [quantity]x[price] [item]` or `Edit [item#] [price] [item]`\n"
        send_list()

    elif message.arguments[1].casefold() == "Clear".casefold():
        if len(message.arguments) > 2:
            items_in_list = Kharchey.objects.filter(group=message.group, sender=message.sender).order_by("date")
            for item_no in message.arguments[2:]:
                if item_no.isdigit() and int(item_no) <= len(items_in_list):
                    item = items_in_list[int(item_no) - 1]
                    item.delete()
        elif len(message.arguments) == 2:
            Kharchey.objects.filter(group=message.group, sender=message.sender).delete()
        else:
            message.outgoing_text_message = "Usage: `Clear [item1#] [item2#] ...`\n"
        send_list()

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
        if failed:
            message.outgoing_text_message += f"Failed to add *{', '.join(failed)}* to list\n"
            message.outgoing_text_message += "Usage: `[quantity]x[price] [item]`\n"
        if success:
            send_list()
