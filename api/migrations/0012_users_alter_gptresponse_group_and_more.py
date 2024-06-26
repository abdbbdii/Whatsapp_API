# Generated by Django 4.2.9 on 2024-06-27 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0011_settings_reminders_api_remind_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Users",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.TextField(default=None, null=True)),
                ("group_id", models.TextField(default=None, null=True)),
                ("description", models.JSONField(default=None, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name="gptresponse",
            name="group",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="gptresponse",
            name="message",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="gptresponse",
            name="response",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="gptresponse",
            name="sender",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="kharchey",
            name="group",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="kharchey",
            name="item",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="kharchey",
            name="sender",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="settings",
            name="admin_command_prefix",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="settings",
            name="admin_ids",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="settings",
            name="blacklist_ids",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="settings",
            name="classroom_group_id",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="settings",
            name="classroom_group_id_test",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="settings",
            name="google_credentials",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="settings",
            name="kharchey_group_id",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="settings",
            name="ocr_space_api_key",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="settings",
            name="openai_api_key",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="settings",
            name="public_url",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="settings",
            name="public_url_test",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="settings",
            name="reminders_api_classroom_id",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="settings",
            name="reminders_api_classroom_id_test",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="settings",
            name="reminders_api_classroom_name",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="settings",
            name="reminders_api_classroom_name_test",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="settings",
            name="reminders_api_remind_id",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="settings",
            name="reminders_key",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="settings",
            name="token_pickle_base64",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="settings",
            name="whatsapp_client_url",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="settings",
            name="whatsapp_client_url_test",
            field=models.TextField(default=None, null=True),
        ),
    ]
