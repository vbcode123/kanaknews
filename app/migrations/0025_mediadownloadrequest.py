# Generated for MediaDownloadRequest feature
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_alter_deskvoiceoverchatmessage_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaDownloadRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requester_name', models.CharField(help_text='Name of staff requesting download', max_length=150)),
                ('role_name', models.CharField(default='Staff', help_text='Role: Desk, Visual Editor, etc.', max_length=50)),
                ('file_url', models.TextField(help_text='URL of media file being requested')),
                ('file_name', models.CharField(help_text='Clean display name of the file/story', max_length=255)),
                ('passcode', models.CharField(help_text='6-digit auto-generated passcode', max_length=6)),
                ('is_approved', models.BooleanField(default=False, help_text='True if approved by Admin/Chief Editor')),
                ('is_used', models.BooleanField(default=False, help_text='True once successfully downloaded')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(help_text='Expiry time (e.g. +15 mins)')),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_downloads', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='download_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Media Download Request',
                'verbose_name_plural': 'Media Download Requests',
                'db_table': 'app_mediadownloadrequest',
                'ordering': ['-created_at'],
            },
        ),
    ]
