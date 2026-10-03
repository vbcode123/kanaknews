# Generated manually for Desk - Copy Editor Chat feature

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_desk_visual_editor_chat'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DeskCopyChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_type', models.CharField(choices=[('desk', 'Desk'), ('copy_editor', 'Copy Editor')], help_text='Sender role: desk or copy_editor', max_length=20)),
                ('message', models.TextField(help_text='Message text content')),
                ('attachment', models.FileField(blank=True, help_text='Optional attached file or image', null=True, upload_to='chat_attachments/')),
                ('is_read', models.BooleanField(default=False, help_text='True if read by recipient')),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('desk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='copy_editor_chat_messages', to='app.desk')),
                ('sender_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_desk_ce_messages', to=settings.AUTH_USER_MODEL)),
                ('copy_editor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='desk_chat_messages', to='app.copyeditor')),
            ],
            options={
                'verbose_name': 'Desk-Copy Editor Chat Message',
                'verbose_name_plural': 'Desk-Copy Editor Chat Messages',
                'db_table': 'app_deskcopychatmessage',
                'ordering': ['created_at'],
            },
        ),
    ]
