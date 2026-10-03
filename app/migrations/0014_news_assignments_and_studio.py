import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_visualeditor'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='edited_video',
            field=models.FileField(blank=True, help_text='Final rendered news video from Studio', null=True, upload_to='edited_news_videos/'),
        ),
        migrations.AddField(
            model_name='news',
            name='is_video_edited_by_desk',
            field=models.BooleanField(default=False, help_text='True if Desk staff edited the video'),
        ),
        migrations.AddField(
            model_name='news',
            name='edited_at',
            field=models.DateTimeField(blank=True, help_text='Timestamp when video was edited in studio', null=True),
        ),
        migrations.AddField(
            model_name='news',
            name='assigned_copy_editor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_news', to='app.copyeditor'),
        ),
        migrations.AddField(
            model_name='news',
            name='assigned_visual_editor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_news', to='app.visualeditor'),
        ),
        migrations.AddField(
            model_name='news',
            name='assigned_voice_over',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_news', to='app.voiceoveruser'),
        ),
        migrations.AddField(
            model_name='news',
            name='assigned_graphic_designer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_news', to='app.graphicdesigner'),
        ),
        migrations.AddField(
            model_name='news',
            name='desk_notes',
            field=models.TextField(blank=True, help_text='Desk instructions to assigned staff', null=True),
        ),
        migrations.AddField(
            model_name='news',
            name='assigned_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='news',
            name='sent_to_social_media',
            field=models.BooleanField(default=False, help_text='True if story is sent to Social Media team'),
        ),
        migrations.AddField(
            model_name='news',
            name='sent_to_social_media_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
