# import json
# from argparse import ArgumentParser

# from api.utils.reminders_api import ReminderAPI
# from api.whatsapp_api_handle import Message
# from api.appSettings import appSettings

# pluginInfo = {
#     "command_name": "remind",
#     "description": "Set a reminder for a specific date and time.",
#     "admin_privilege": False,
#     "internal": False,
# }


# def handle_function(message: Message):
#     if message.document:
#     try:
#         if len(message.arguments) == 1:
#             raise SystemExit
#         parsed = parser(message.arguments)

#     except SystemExit:
#         pretext = message.command_prefix + (appSettings.admin_command_prefix + " " if pluginInfo["admin_privilege"] else "") + pluginInfo["command_name"]
#         message.outgoing_text_message = f"""*Usage:*
# - `Reminder: {pretext} -d [YYYY-MM-DD] -t [HH:MM] -m [message]`
# - `Reminder with recurrence rule: {pretext} -d [YYYY-MM-DD] -t [HH:MM] -r [RRULE] -m [message]`
# """
#         message.send_message()
#         return

#     reminders_api = ReminderAPI(appSettings.reminders_key, appSettings.public_url + "api/reminder", ("admin", "admin"))
#     if appSettings.reminders_api_remind_id and reminders_api.get_application(appSettings.reminders_api_remind_id).json().get("message") != "Item not found.":
#         application_id = appSettings.reminders_api_remind_id
#     else:
#         application_id = reminders_api.find_application_id(appSettings.reminders_api_classroom_name)
#         if not application_id:
#             application_id = reminders_api.create_application(appSettings.reminders_api_classroom_name, "10:00").json().get("id")
#         appSettings.update("reminders_api_remind_id", application_id)

#     response = reminders_api.create_reminder(
#         application_id=application_id,
#         title=parsed.message,
#         timezone="Asia/Karachi",
#         date_tz=parsed.date,
#         time_tz=parsed.time,
#         notes=json.dumps({"from": "remind", "sender": message.send_to[0]}),
#         rrule=parsed.rrule,
#         webhook_url=appSettings.public_url + "api/reminder",
#     )
#     print(response.text)
#     message.outgoing_text_message = "Reminder set successfully."
#     message.send_message()


# def parser(args: str) -> ArgumentParser:
#     parser = ArgumentParser(description="Set a reminder for a specific date and time.")
#     parser.add_argument("-d", "--date", type=str, help="Date in the format YYYY-MM-DD.")
#     parser.add_argument("-t", "--time", type=str, help="Time in the format HH:MM.")
#     parser.add_argument("-r", "--rrule", type=str, help="Recurrence rule.")
#     parser.add_argument("-m", "--message", type=str, help="Message to remind.")
#     return parser.parse_args(args)
