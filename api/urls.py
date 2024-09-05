from django.urls import path
from . import views

urlpatterns = [
    path("whatsapp", views.whatsapp, name="whatsapp"),
    path("classroom", views.classroom, name="classroom"),
    path("reminder", views.reminder, name="reminder"),
]