# Generated manually for Desk - Reporter Chat feature

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_desk_social_media_chat'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='reporter',
            name='last_seen',
            field=models.DateTimeField(blank=True, help_text='Last active timestamp', null=True),
        ),
        migrations.CreateModel(
            name='DeskReporterChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_type', models.CharField(choices=[('desk', 'Desk'), ('reporter', 'Reporter')], help_text='Sender role: desk or reporter', max_length=20)),
                ('message', models.TextField(help_text='Message text content')),
                ('attachment', models.FileField(blank=True, help_text='Optional attached file or image', null=True, upload_to='chat_attachments/')),
                ('is_read', models.BooleanField(default=False, help_text='True if read by recipient')),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('desk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporter_chat_messages', to='app.desk')),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='desk_chat_messages', to='app.reporter')),
                ('sender_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_desk_rep_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Desk-Reporter Chat Message',
                'verbose_name_plural': 'Desk-Reporter Chat Messages',
                'db_table': 'app_deskreporterchatmessage',
                'ordering': ['created_at'],
            },
        ),
    ]
