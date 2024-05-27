from api.whatsapp_api_handle import Message
from argparse import ArgumentParser
import shlex
from datetime import datetime, timedelta


pluginInfo = {
    "command_name": "calender",
    "admin_privilege": True,
    "description": "Calender commands to manage calender. Use ```/abd calender help``` to see available commands",
    "internal": False,
}


def handle_function(message: Message):
    ...

def parser(input: str):
    parser = ArgumentParser(description="Add events to google calender.")
    parser.add_argument("--title", type=str, help="Title of an event.", required=True)
    parser.add_argument("--from", type=datetime, help="Datetime object to specify the starting date of an event.", required=True)
    parser.add_argument("--for", type=timedelta, help="Timedelta object to specify the duration of the event.")
    parser.add_argument("--to", type=datetime, help="Datetime object to specify the ending date of an event.")
    parser.add_argument("--repeat", type=str, choices=["daily", "weekly", "monthly", "yearly"], help="How the event should repeat.")
    parser.add_argument("--allday", action="store_true", help="Bool tag to specify if the the event would last all day.")
    parser.add_argument("--days", type=datetime.weekday, nargs="+", help="Weekday object to specify in what day the event is.")
    parser.add_argument("--color", type=str, help="Hex code or name of a color.")
    parser.add_argument("--description", type=str, help="Description of the Event.")
    parser.add_argument("--get", action="store_true", help="Get all the events.")
    try:
        args = parser.parse_args(shlex.split(input))
    except SystemExit:
        return parser.format_help()
    return args
