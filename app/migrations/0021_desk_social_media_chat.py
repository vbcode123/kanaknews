# Generated manually for Desk - Social Media Chat feature

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_add_last_seen_to_staff'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='socialmedia',
            name='last_seen',
            field=models.DateTimeField(blank=True, help_text='Last active timestamp', null=True),
        ),
        migrations.CreateModel(
            name='DeskSocialChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_type', models.CharField(choices=[('desk', 'Desk'), ('social_media', 'Social Media')], help_text='Sender role: desk or social_media', max_length=20)),
                ('message', models.TextField(help_text='Message text content')),
                ('attachment', models.FileField(blank=True, help_text='Optional attached file or image', null=True, upload_to='chat_attachments/')),
                ('is_read', models.BooleanField(default=False, help_text='True if read by recipient')),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('desk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_media_chat_messages', to='app.desk')),
                ('sender_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_desk_sm_messages', to=settings.AUTH_USER_MODEL)),
                ('social_media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='desk_chat_messages', to='app.socialmedia')),
            ],
            options={
                'verbose_name': 'Desk-Social Media Chat Message',
                'verbose_name_plural': 'Desk-Social Media Chat Messages',
                'db_table': 'app_desksocialchatmessage',
                'ordering': ['created_at'],
            },
        ),
    ]
