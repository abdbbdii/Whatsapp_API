from django.http import JsonResponse
from api.whatsapp_api_handle import API
import json
from .appSettings import appSettings

def whatsapp(request):
    if request.method == "POST":
        print("POST /api/whatsapp")
        # print(json.loads(request.body.decode("utf-8")))
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
                "from": f"{appSettings.admin_ids[0]}@s.whatsapp.net in {appSettings.classroom_group_id}@g.us",
                "message": {"text": "./classroom"},
            }
        )
        return JsonResponse({"statusCode": 200, "message": "Notification sent successfully."})
    else:
        return JsonResponse({"message": "Authorization required."})


def reminder(request):
    if request.method == "POST":
        print("POST /api/reminder")
        API(
            {
                "document": json.loads(request.body.decode("utf-8")),
                "from": f"{appSettings.admin_ids[0]}@s.whatsapp.net in {appSettings.classroom_group_id}@g.us",
                "message": {"text": "./reminder"},
            }
        )
        return JsonResponse({"statusCode": 200, "message": "Reminder sent successfully."})
    else:
        return JsonResponse({"message": "Authorization required."})
