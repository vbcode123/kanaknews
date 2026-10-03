# Generated for TeleprompterScript and Graphic Designer fields on News

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_desk_reporter_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='is_graphics_completed',
            field=models.BooleanField(default=False, help_text='True if Graphic Designer has prepared graphics and sent to Visual Editor'),
        ),
        migrations.AddField(
            model_name='news',
            name='graphics_sent_to_visual_editor_at',
            field=models.DateTimeField(blank=True, help_text='Timestamp when Graphic Designer sent graphics to Visual Editor', null=True),
        ),
        migrations.CreateModel(
            name='TeleprompterScript',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', help_text='Headline or Topic of Teleprompter', max_length=255)),
                ('script_text', models.TextField(help_text='Odia, English, or Hindi teleprompter script narrative')),
                ('is_read', models.BooleanField(default=False, help_text='True if viewed by reporter')),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('desk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_teleprompter_scripts', to='app.desk')),
                ('news', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teleprompter_scripts', to='app.news')),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teleprompter_scripts', to='app.reporter')),
            ],
            options={
                'verbose_name': 'Teleprompter Script',
                'verbose_name_plural': 'Teleprompter Scripts',
                'db_table': 'app_teleprompterscript',
                'ordering': ['-created_at'],
            },
        ),
    ]
