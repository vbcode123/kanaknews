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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Reporter"
        verbose_name_plural = "Reporters"
        ordering = ['-created_at']

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Desk"
        verbose_name_plural = "Desks"
        ordering = ['-created_at']

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
    status = models.CharField(max_length=30, choices=NEWS_STATUS_CHOICES, default='Submitted')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ['-created_at']

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
