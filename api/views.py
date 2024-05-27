from django.http import JsonResponse
from .whatsapp_api_handle import API, appSettings
import json, os


# Path: /api/whatsapp
def whatsapp(request):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        print("WhatsApp API")
        API(body)
        print("Message sent successfully.")
        return JsonResponse({"statusCode": 200, "message": "Message sent successfully."})
    else:
        return JsonResponse({"message": "Authorization required."})


# Path: /api/classroom
def classroom(request):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        print("Classroom API")
        API(
            {
                "document": body,
                "from": f"{appSettings["adminIds"][0]}@s.whatsapp.net in {appSettings['classroomGroupId']}",
                "message": {"text": "./classroom"},
            }
        )
        print("Notification sent successfully.")
        return JsonResponse({"statusCode": 200, "message": "Notification sent successfully."})
    else:
        return JsonResponse({"message": "Authorization required."})


# Path: /api/reminder
def reminder(request):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        print("Reminder API")
        print(body)
        API(
            {
                "document": body,
                "from": f"{appSettings["adminIds"][0]}@s.whatsapp.net in {appSettings['classroomGroupId']}",
                "message": {"text": "./reminder"},
            }
        )
        print("Reminder sent successfully.")
        return JsonResponse({"statusCode": 200, "message": "Reminder sent successfully."})
    else:
        return JsonResponse({"message": "Authorization required."})
