from django.http import JsonResponse
from api.whatsapp_api_handle import API
import json
from .appSettings import appSettings

def whatsapp(request):
    if request.method == "POST":
        print("/api/whatsapp")
        API(json.loads(request.body.decode("utf-8")))
        print("Message sent successfully.")
        return JsonResponse({"statusCode": 200, "message": "Message sent successfully."})
    else:
        return JsonResponse({"message": "Authorization required."})


def classroom(request):
    if request.method == "POST":
        print("/api/classroom")
        API(
            {
                "document": json.loads(request.body.decode("utf-8")),
                "from": f"{appSettings.admin_ids[0]}@s.whatsapp.net in {appSettings.classroom_group_id}",
                "message": {"text": "./classroom"},
            }
        )
        print("Notification sent successfully.")
        return JsonResponse({"statusCode": 200, "message": "Notification sent successfully."})
    else:
        return JsonResponse({"message": "Authorization required."})


def reminder(request):
    if request.method == "POST":
        print("/api/reminder")
        API(
            {
                "document": json.loads(request.body.decode("utf-8")),
                "from": f"{appSettings.admin_ids[0]}@s.whatsapp.net in {appSettings.classroom_group_id}@g.us",
                "message": {"text": "./reminder"},
            }
        )
        print("Reminder sent successfully.")
        return JsonResponse({"statusCode": 200, "message": "Reminder sent successfully."})
    else:
        return JsonResponse({"message": "Authorization required."})
