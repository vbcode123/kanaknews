from django.db import models
from django.contrib.auth.models import User


def generate_next_reporter_id():
    """
    Generates the next unique Reporter ID in the format NL_<number>,
    starting at NL_1001 or incrementing from the highest existing NL_ number.
    """
    reporters = Reporter.objects.filter(reporter_id__startswith='NL_')
    max_num = 1000
    for r in reporters:
        if r.reporter_id:
            suffix = r.reporter_id[3:].strip()
            if suffix.isdigit():
                val = int(suffix)
                if val > max_num:
                    max_num = val
    return f"NL_{max_num + 1}"


class Reporter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reporter_profile')
    reporter_id = models.CharField(
        max_length=30, 
        unique=True, 
        blank=True, 
        null=True, 
        db_index=True, 
        help_text="Official Reporter ID (e.g. NL_1001)"
    )
    name = models.CharField(max_length=150, help_text="Full Name of the Reporter")
    phone_number = models.CharField(max_length=20, unique=True, help_text="Login Phone Number")
    address = models.TextField(help_text="Full Residential / Office Address")
    district = models.CharField(max_length=100, help_text="Assigned District / Location")
    aadhar_image = models.ImageField(upload_to='aadhar_images/', blank=True, null=True, help_text="Aadhar Card Document Image")
    profile_image = models.ImageField(upload_to='reporter_profiles/', blank=True, null=True, help_text="Reporter Passport/Profile Photo")
    is_active = models.BooleanField(default=True, help_text="Account Active Status")
    last_seen = models.DateTimeField(null=True, blank=True, help_text="Last active timestamp")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Reporter"
        verbose_name_plural = "Reporters"
        ordering = ['-created_at']

    def get_last_seen_info(self):
        from django.utils import timezone
        from datetime import timedelta
        last = self.last_seen
        if not last and hasattr(self, 'user') and self.user:
            last = getattr(self.user, 'last_login', None)
        if not last:
            return {'is_online': False, 'text': 'Offline'}
        now = timezone.now()
        diff = (now - last).total_seconds()
        if diff < 120:
            return {'is_online': True, 'text': 'Online'}
        elif last.date() == now.date():
            return {'is_online': False, 'text': f"Last seen today at {last.strftime('%I:%M %p')}"}
        elif last.date() == (now - timedelta(days=1)).date():
            return {'is_online': False, 'text': f"Last seen yesterday at {last.strftime('%I:%M %p')}"}
        else:
            return {'is_online': False, 'text': f"Last seen on {last.strftime('%d %b, %I:%M %p')}"}

    def save(self, *args, **kwargs):
        if not self.reporter_id:
            self.reporter_id = generate_next_reporter_id()
        super().save(*args, **kwargs)

    def __str__(self):
        rep_id = f" [{self.reporter_id}]" if self.reporter_id else ""
        return f"{self.name}{rep_id} ({self.district} - {self.phone_number})"


class Desk(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='desk_profile')
    name = models.CharField(max_length=150, help_text="Full Name of the Desk Staff")
    phone_number = models.CharField(max_length=20, unique=True, help_text="Login Phone Number")
    email = models.EmailField(max_length=255, unique=True, help_text="Gmail / Email Address")
    is_active = models.BooleanField(default=True, help_text="Account Active Status")
    last_seen = models.DateTimeField(null=True, blank=True, help_text="Last active timestamp")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Desk"
        verbose_name_plural = "Desks"
        ordering = ['-created_at']

    def get_last_seen_info(self):
        from django.utils import timezone
        from datetime import timedelta
        last = self.last_seen
        if not last and hasattr(self, 'user') and self.user:
            last = getattr(self.user, 'last_login', None)
        if not last:
            return {'is_online': False, 'text': 'Offline'}
        now = timezone.now()
        diff = (now - last).total_seconds()
        if diff < 120:
            return {'is_online': True, 'text': 'Online'}
        elif last.date() == now.date():
            return {'is_online': False, 'text': f"Last seen today at {last.strftime('%I:%M %p')}"}
        elif last.date() == (now - timedelta(days=1)).date():
            return {'is_online': False, 'text': f"Last seen yesterday at {last.strftime('%I:%M %p')}"}
        else:
            return {'is_online': False, 'text': f"Last seen on {last.strftime('%d %b, %I:%M %p')}"}

    def __str__(self):
        return f"{self.name} ({self.phone_number})"


class SocialMedia(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='social_media_profile')
    name = models.CharField(max_length=150, help_text="Full Name of the Social Media Staff")
    phone_number = models.CharField(max_length=20, unique=True, help_text="Login Phone Number")
    is_active = models.BooleanField(default=True, help_text="Account Active Status")
    last_seen = models.DateTimeField(null=True, blank=True, help_text="Last active timestamp")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Social Media"
        verbose_name_plural = "Social Media Staff"
        ordering = ['-created_at']

    def get_last_seen_info(self):
        from django.utils import timezone
        from datetime import timedelta
        last = self.last_seen
        if not last and hasattr(self, 'user') and self.user:
            last = getattr(self.user, 'last_login', None)
        if not last:
            return {'is_online': False, 'text': 'Offline'}
        now = timezone.now()
        diff = (now - last).total_seconds()
        if diff < 120:
            return {'is_online': True, 'text': 'Online'}
        elif last.date() == now.date():
            return {'is_online': False, 'text': f"Last seen today at {last.strftime('%I:%M %p')}"}
        elif last.date() == (now - timedelta(days=1)).date():
            return {'is_online': False, 'text': f"Last seen yesterday at {last.strftime('%I:%M %p')}"}
        else:
            return {'is_online': False, 'text': f"Last seen on {last.strftime('%d %b, %I:%M %p')}"}

    def __str__(self):
        return f"{self.name} ({self.phone_number})"


class GraphicDesigner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='graphic_designer_profile')
    name = models.CharField(max_length=150, help_text="Full Name of the Graphic Designer")
    phone_number = models.CharField(max_length=20, unique=True, help_text="Login Phone Number")
    is_active = models.BooleanField(default=True, help_text="Account Active Status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Graphic Designer"
        verbose_name_plural = "Graphic Designers"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.phone_number})"


class InputUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='input_profile')
    name = models.CharField(max_length=150, help_text="Full Name of the Input Staff")
    phone_number = models.CharField(max_length=20, unique=True, help_text="Login Phone Number")
    is_active = models.BooleanField(default=True, help_text="Account Active Status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Input"
        verbose_name_plural = "Inputs"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.phone_number})"


# Convenient alias
Input = InputUser


class VoiceOverUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='voice_over_profile')
    name = models.CharField(max_length=150, help_text="Full Name of the Voice Over Staff")
    phone_number = models.CharField(max_length=20, unique=True, help_text="Login Phone Number")
    is_active = models.BooleanField(default=True, help_text="Account Active Status")
    last_seen = models.DateTimeField(null=True, blank=True, help_text="Last active timestamp")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Voice Over"
        verbose_name_plural = "Voice Overs"
        ordering = ['-created_at']

    def get_last_seen_info(self):
        from django.utils import timezone
        from datetime import timedelta
        last = self.last_seen
        if not last and hasattr(self, 'user') and self.user:
            last = getattr(self.user, 'last_login', None)
        if not last:
            return {'is_online': False, 'text': 'Offline'}
        now = timezone.now()
        diff = (now - last).total_seconds()
        if diff < 120:
            return {'is_online': True, 'text': 'Online'}
        elif last.date() == now.date():
            return {'is_online': False, 'text': f"Last seen today at {last.strftime('%I:%M %p')}"}
        elif last.date() == (now - timedelta(days=1)).date():
            return {'is_online': False, 'text': f"Last seen yesterday at {last.strftime('%I:%M %p')}"}
        else:
            return {'is_online': False, 'text': f"Last seen on {last.strftime('%d %b, %I:%M %p')}"}

    def __str__(self):
        return f"{self.name} ({self.phone_number})"


# Convenient aliases
VoiceOver = VoiceOverUser
VoiceHover = VoiceOverUser


class CopyEditor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='copy_editor_profile')
    name = models.CharField(max_length=150, help_text="Full Name of the Copy Editor")
    phone_number = models.CharField(max_length=20, unique=True, help_text="Login Phone Number")
    is_active = models.BooleanField(default=True, help_text="Account Active Status")
    last_seen = models.DateTimeField(null=True, blank=True, help_text="Last active timestamp")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Copy Editor"
        verbose_name_plural = "Copy Editors"
        ordering = ['-created_at']

    def get_last_seen_info(self):
        from django.utils import timezone
        from datetime import timedelta
        last = self.last_seen
        if not last and hasattr(self, 'user') and self.user:
            last = getattr(self.user, 'last_login', None)
        if not last:
            return {'is_online': False, 'text': 'Offline'}
        now = timezone.now()
        diff = (now - last).total_seconds()
        if diff < 120:
            return {'is_online': True, 'text': 'Online'}
        elif last.date() == now.date():
            return {'is_online': False, 'text': f"Last seen today at {last.strftime('%I:%M %p')}"}
        elif last.date() == (now - timedelta(days=1)).date():
            return {'is_online': False, 'text': f"Last seen yesterday at {last.strftime('%I:%M %p')}"}
        else:
            return {'is_online': False, 'text': f"Last seen on {last.strftime('%d %b, %I:%M %p')}"}

    def __str__(self):
        return f"{self.name} ({self.phone_number})"


class VisualEditor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='visual_editor_profile')
    name = models.CharField(max_length=150, help_text="Full Name of the Visual Editor")
    phone_number = models.CharField(max_length=20, unique=True, help_text="Login Phone Number")
    is_active = models.BooleanField(default=True, help_text="Account Active Status")
    last_seen = models.DateTimeField(null=True, blank=True, help_text="Last active timestamp")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Visual Editor"
        verbose_name_plural = "Visual Editors"
        ordering = ['-created_at']

    def get_last_seen_info(self):
        from django.utils import timezone
        from datetime import timedelta
        last = self.last_seen
        if not last and hasattr(self, 'user') and self.user:
            last = getattr(self.user, 'last_login', None)
        if not last:
            return {'is_online': False, 'text': 'Offline'}
        now = timezone.now()
        diff = (now - last).total_seconds()
        if diff < 120:
            return {'is_online': True, 'text': 'Online'}
        elif last.date() == now.date():
            return {'is_online': False, 'text': f"Last seen today at {last.strftime('%I:%M %p')}"}
        elif last.date() == (now - timedelta(days=1)).date():
            return {'is_online': False, 'text': f"Last seen yesterday at {last.strftime('%I:%M %p')}"}
        else:
            return {'is_online': False, 'text': f"Last seen on {last.strftime('%d %b, %I:%M %p')}"}

    def __str__(self):
        return f"{self.name} ({self.phone_number})"


NEWS_TYPE_CHOICES = [
    ('AVO', 'AVO'),
    ('Byte', 'Byte'),
    ('AVO Byte', 'AVO Byte'),
    ('PKG', 'PKG'),
]

NEWS_CATEGORY_CHOICES = [
    ('Breaking News', 'Breaking News'),
    ('Politics', 'Politics'),
    ('Crime & Law', 'Crime & Law'),
    ('Accident & Disaster', 'Accident & Disaster'),
    ('Local & Regional', 'Local & Regional'),
    ('Development & Infra', 'Development & Infra'),
    ('Sports', 'Sports'),
    ('Entertainment', 'Entertainment'),
    ('Business & Economy', 'Business & Economy'),
    ('Health & Education', 'Health & Education'),
    ('General', 'General'),
]

NEWS_STATUS_CHOICES = [
    ('Submitted', 'Submitted'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
]


class News(models.Model):
    headline = models.CharField(max_length=300, help_text="News Headline / Title")
    news_type = models.CharField(max_length=50, choices=NEWS_TYPE_CHOICES, help_text="News Format Type")
    category = models.CharField(max_length=100, choices=NEWS_CATEGORY_CHOICES, default='General')
    location = models.CharField(max_length=200, help_text="Incident Location / Landmark")
    district = models.CharField(max_length=100, help_text="Assigned District")
    description = models.TextField(help_text="Detailed News Description / Script")
    media_file = models.FileField(upload_to='news_media/', blank=True, null=True, help_text="Main Video or Image File")
    byte_interview = models.TextField(blank=True, null=True, help_text="Optional Byte / Interview Details")
    byte_media = models.FileField(upload_to='news_bytes/', blank=True, null=True, help_text="Optional Byte Audio / Video File")
    reporter = models.ForeignKey(Reporter, on_delete=models.SET_NULL, null=True, blank=True, related_name='news_reports')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_news')
    # Studio & Editing fields
    edited_video = models.FileField(upload_to='edited_news_videos/', blank=True, null=True, help_text="Final rendered news video from Studio")
    is_video_edited_by_desk = models.BooleanField(default=False, help_text="True if Desk staff edited the video")
    edited_at = models.DateTimeField(null=True, blank=True, help_text="Timestamp when video was edited in studio")

    # Team Assignment fields
    assigned_copy_editor = models.ForeignKey(CopyEditor, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_news')
    is_script_edited_by_copy_editor = models.BooleanField(default=False, help_text="True if Copy Editor has edited and forwarded script to Visual Editor")
    sent_to_visual_editor_at = models.DateTimeField(null=True, blank=True, help_text="Timestamp when Copy Editor forwarded script to Visual Editor")
    assigned_visual_editor = models.ForeignKey(VisualEditor, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_news')
    assigned_voice_over = models.ForeignKey(VoiceOverUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_news')
    assigned_graphic_designer = models.ForeignKey(GraphicDesigner, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_news')
    is_graphics_completed = models.BooleanField(default=False, help_text="True if Graphic Designer has prepared graphics and sent to Visual Editor")
    graphics_sent_to_visual_editor_at = models.DateTimeField(null=True, blank=True, help_text="Timestamp when Graphic Designer sent graphics to Visual Editor")
    desk_notes = models.TextField(blank=True, null=True, help_text="Desk instructions to assigned staff")
    assigned_at = models.DateTimeField(null=True, blank=True)

    # Social Media Dispatch
    assigned_social_media = models.ForeignKey(SocialMedia, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_news')
    sent_to_social_media = models.BooleanField(default=False, help_text="True if story is sent to Social Media team")
    sent_to_social_media_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=30, choices=NEWS_STATUS_CHOICES, default='Submitted')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.status == 'Rejected':
            # Delete media files from storage when story is rejected
            if self.media_file:
                try:
                    self.media_file.delete(save=False)
                except Exception:
                    pass
                self.media_file = None
            if self.byte_media:
                try:
                    self.byte_media.delete(save=False)
                except Exception:
                    pass
                self.byte_media = None
            if self.pk:
                for extra in self.additional_media.all():
                    try:
                        extra.file.delete(save=False)
                    except Exception:
                        pass
                    extra.delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.news_type}] {self.headline} ({self.district})"

    @property
    def is_video(self):
        if self.media_file:
            import os
            ext = os.path.splitext(self.media_file.name)[1].lower()
            return ext in ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv', '.wmv', '.3gp', '.m4v']
        return False

    @property
    def is_image(self):
        if self.media_file:
            import os
            ext = os.path.splitext(self.media_file.name)[1].lower()
            return ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.svg']
        return False

    @property
    def total_media_count(self):
        count = 1 if self.media_file else 0
        if self.pk:
            count += self.additional_media.count()
        return count

    @property
    def byte_is_video(self):
        if self.byte_media:
            import os
            ext = os.path.splitext(self.byte_media.name)[1].lower()
            return ext in ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv', '.wmv']
        return False

    @property
    def byte_is_audio(self):
        if self.byte_media:
            import os
            ext = os.path.splitext(self.byte_media.name)[1].lower()
            return ext in ['.mp3', '.wav', '.ogg', '.m4a', '.aac']
        return False

    @property
    def has_edited_video(self):
        return bool(self.edited_video and hasattr(self.edited_video, 'name') and self.edited_video.name)


class NewsMedia(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='additional_media')
    file = models.FileField(upload_to='news_media/', help_text="Additional Video or Image File")
    caption = models.CharField(max_length=255, blank=True, null=True, help_text="Optional caption or note")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "News Media"
        verbose_name_plural = "News Media Files"
        ordering = ['created_at']

    def __str__(self):
        return f"Media for {self.news.headline} ({self.file.name})"

    @property
    def is_video(self):
        if self.file:
            import os
            ext = os.path.splitext(self.file.name)[1].lower()
            return ext in ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv', '.wmv', '.3gp', '.m4v']
        return False

    @property
    def is_image(self):
        if self.file:
            import os
            ext = os.path.splitext(self.file.name)[1].lower()
            return ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.svg']
        return False

    @property
    def file_extension(self):
        if self.file:
            import os
            return os.path.splitext(self.file.name)[1].lower().replace('.', '').upper()
        return ''


class TeleprompterScript(models.Model):
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE, related_name='teleprompter_scripts')
    desk = models.ForeignKey(Desk, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_teleprompter_scripts')
    title = models.CharField(max_length=255, blank=True, default='', help_text="Headline or Topic of Teleprompter")
    script_text = models.TextField(help_text="Odia, English, or Hindi teleprompter script narrative")
    news = models.ForeignKey(News, on_delete=models.SET_NULL, null=True, blank=True, related_name='teleprompter_scripts')
    is_read = models.BooleanField(default=False, help_text="True if viewed by reporter")
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'app_teleprompterscript'
        verbose_name = "Teleprompter Script"
        verbose_name_plural = "Teleprompter Scripts"
        ordering = ['-created_at']

    def __str__(self):
        rep_name = self.reporter.name if self.reporter else "Reporter"
        return f"Prompter #{self.pk} for {rep_name} - {self.title[:30]}"


class DeskVisualChatMessage(models.Model):
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE, related_name='visual_editor_chat_messages')
    visual_editor = models.ForeignKey(VisualEditor, on_delete=models.CASCADE, related_name='desk_chat_messages')
    sender_type = models.CharField(
        max_length=20,
        choices=[('desk', 'Desk'), ('visual_editor', 'Visual Editor')],
        help_text="Sender role: desk or visual_editor"
    )
    sender_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_desk_ve_messages')
    message = models.TextField(help_text="Message text content")
    attachment = models.FileField(upload_to='chat_attachments/', blank=True, null=True, help_text="Optional attached file or image")
    is_read = models.BooleanField(default=False, help_text="True if read by recipient")
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'app_deskvisualchatmessage'
        verbose_name = "Desk-Visual Editor Chat Message"
        verbose_name_plural = "Desk-Visual Editor Chat Messages"
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.sender_type.upper()}] {self.desk.name} <-> {self.visual_editor.name}: {self.message[:30]}"


class DeskCopyChatMessage(models.Model):
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE, related_name='copy_editor_chat_messages')
    copy_editor = models.ForeignKey(CopyEditor, on_delete=models.CASCADE, related_name='desk_chat_messages')
    sender_type = models.CharField(
        max_length=20,
        choices=[('desk', 'Desk'), ('copy_editor', 'Copy Editor')],
        help_text="Sender role: desk or copy_editor"
    )
    sender_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_desk_ce_messages')
    message = models.TextField(help_text="Message text content")
    attachment = models.FileField(upload_to='chat_attachments/', blank=True, null=True, help_text="Optional attached file or image")
    is_read = models.BooleanField(default=False, help_text="True if read by recipient")
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'app_deskcopychatmessage'
        verbose_name = "Desk-Copy Editor Chat Message"
        verbose_name_plural = "Desk-Copy Editor Chat Messages"
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.sender_type.upper()}] {self.desk.name} <-> {self.copy_editor.name}: {self.message[:30]}"


class DeskVoiceOverChatMessage(models.Model):
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE, related_name='voice_over_chat_messages')
    voice_over = models.ForeignKey(VoiceOverUser, on_delete=models.CASCADE, related_name='desk_chat_messages')
    sender_type = models.CharField(
        max_length=20,
        choices=[('desk', 'Desk'), ('voice_over', 'Voice Hover')],
        help_text="Sender role: desk or voice_over"
    )
    sender_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_desk_vo_messages')
    message = models.TextField(help_text="Message text content")
    attachment = models.FileField(upload_to='chat_attachments/', blank=True, null=True, help_text="Optional attached audio, script, or image")
    is_read = models.BooleanField(default=False, help_text="True if read by recipient")
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'app_deskvoiceoverchatmessage'
        verbose_name = "Desk-Voice Hover Chat Message"
        verbose_name_plural = "Desk-Voice Hover Chat Messages"
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.sender_type.upper()}] {self.desk.name} <-> {self.voice_over.name}: {self.message[:30]}"


class DeskSocialChatMessage(models.Model):
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE, related_name='social_media_chat_messages')
    social_media = models.ForeignKey(SocialMedia, on_delete=models.CASCADE, related_name='desk_chat_messages')
    sender_type = models.CharField(
        max_length=20,
        choices=[('desk', 'Desk'), ('social_media', 'Social Media')],
        help_text="Sender role: desk or social_media"
    )
    sender_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_desk_sm_messages')
    message = models.TextField(help_text="Message text content")
    attachment = models.FileField(upload_to='chat_attachments/', blank=True, null=True, help_text="Optional attached file or image")
    is_read = models.BooleanField(default=False, help_text="True if read by recipient")
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'app_desksocialchatmessage'
        verbose_name = "Desk-Social Media Chat Message"
        verbose_name_plural = "Desk-Social Media Chat Messages"
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.sender_type.upper()}] {self.desk.name} <-> {self.social_media.name}: {self.message[:30]}"


class DeskReporterChatMessage(models.Model):
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE, related_name='reporter_chat_messages')
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE, related_name='desk_chat_messages')
    sender_type = models.CharField(
        max_length=20,
        choices=[('desk', 'Desk'), ('reporter', 'Reporter')],
        help_text="Sender role: desk or reporter"
    )
    sender_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_desk_rep_messages')
    message = models.TextField(help_text="Message text content")
    attachment = models.FileField(upload_to='chat_attachments/', blank=True, null=True, help_text="Optional attached file or image")
    is_read = models.BooleanField(default=False, help_text="True if read by recipient")
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'app_deskreporterchatmessage'
        verbose_name = "Desk-Reporter Chat Message"
        verbose_name_plural = "Desk-Reporter Chat Messages"
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.sender_type.upper()}] {self.desk.name} <-> {self.reporter.name}: {self.message[:30]}"



