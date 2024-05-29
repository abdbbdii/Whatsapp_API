from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whatsapp_client_url_test', models.CharField(blank=True, null=True)),
                ('whatsapp_client_url', models.CharField(blank=True, null=True)),
                ('public_url_test', models.CharField(blank=True, null=True)),
                ('public_url', models.CharField(blank=True, null=True)),
                ('admin_ids', models.TextField(blank=True, null=True)),
                ('blacklist_ids', models.TextField(blank=True, null=True)),
                ('admin_command_prefix', models.CharField(blank=True, null=True)),
                ('classroom_group_id_test', models.CharField(blank=True, null=True)),
                ('classroom_group_id', models.CharField(blank=True, null=True)),
                ('reminders_api_classroom_id', models.CharField(blank=True, null=True)),
                ('reminders_key', models.CharField(blank=True, null=True)),
                ('token_pickle_base64', models.TextField(blank=True, null=True)),
                ('google_credentials', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
