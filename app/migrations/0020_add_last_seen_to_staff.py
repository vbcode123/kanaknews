# Generated manually for staff last_seen presence feature

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_desk_voice_over_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='desk',
            name='last_seen',
            field=models.DateTimeField(blank=True, help_text='Last active timestamp', null=True),
        ),
        migrations.AddField(
            model_name='voiceoveruser',
            name='last_seen',
            field=models.DateTimeField(blank=True, help_text='Last active timestamp', null=True),
        ),
        migrations.AddField(
            model_name='copyeditor',
            name='last_seen',
            field=models.DateTimeField(blank=True, help_text='Last active timestamp', null=True),
        ),
        migrations.AddField(
            model_name='visualeditor',
            name='last_seen',
            field=models.DateTimeField(blank=True, help_text='Last active timestamp', null=True),
        ),
    ]
