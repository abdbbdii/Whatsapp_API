# Generated by Django 4.2.9 on 2024-05-29 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_settings_reminders_api_classroom_id_test"),
    ]

    operations = [
        migrations.AddField(
            model_name="settings",
            name="reminders_api_classroom_name",
            field=models.TextField(default="", null=True),
        ),
        migrations.AddField(
            model_name="settings",
            name="reminders_api_classroom_name_test",
            field=models.TextField(default="", null=True),
        ),
    ]
