# Generated by Django 4.2.9 on 2024-06-06 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_settings_openai_api_key"),
    ]

    operations = [
        migrations.AddField(
            model_name="settings",
            name="kharchey_group_id",
            field=models.TextField(default="", null=True),
        ),
    ]
