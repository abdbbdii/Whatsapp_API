from django.http import JsonResponse
from api.whatsapp_api_handle import API
import json
from .appSettings import appSettings

def whatsapp(request):
    if request.method == "POST":
        print("POST /api/whatsapp")
        API(json.loads(request.body.decode("utf-8")))
        return JsonResponse({"statusCode": 200, "message": "Message sent successfully."})
    else:
        return JsonResponse({"message": "Authorization required."})


def classroom(request):
    if request.method == "POST":
        print("POST /api/classroom")
        API(
            {
                "document": json.loads(request.body.decode("utf-8")),
                "document_type": "google_classroom_api",
                "from": f"{appSettings.admin_ids[0]}@s.whatsapp.net in {appSettings.classroom_group_id}@g.us",
            }
        )
        return JsonResponse({"statusCode": 200, "message": "Notification sent successfully."})
    else:
        return JsonResponse({"message": "Authorization required."})


def reminder(request):
    if request.method == "POST":
        print("POST /api/reminder")
        body = json.loads(request.body.decode("utf-8"))

        for reminder in body["reminders_notified"]:
            notes = json.loads(reminder["notes"])
            match str(reminder["application_id"]):
                case appSettings.reminders_api_classroom_id:
                    API(
                        {
                            "document": reminder,
                            "document_type": "reminder_api",
                            "from": f"{appSettings.admin_ids[0]}@s.whatsapp.net in {notes["sender"]}@g.us",
                        }
                    )
                case appSettings.reminders_api_remind_id:
                    API(
                        {
                            "document": reminder,
                            "document_type": "reminder_api",
                            "from": f"{notes["sender"]}@s.whatsapp.net",
                        }
                    )

        return JsonResponse({"statusCode": 200, "message": "Reminder sent successfully."})
    else:
        return JsonResponse({"message": "Authorization required."})
