from django.utils import timezone
from .models import Desk, VoiceOverUser, CopyEditor, VisualEditor, SocialMedia, Reporter


class UserLastSeenMiddleware:
    """
    Middleware that records the last active timestamp for authenticated staff members.
    Throttled to once every 15 seconds per session to prevent database churn.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                now = timezone.now()
                last_ping = request.session.get('last_seen_ping', 0)
                now_ts = now.timestamp()
                # Update every 15 seconds
                if now_ts - last_ping >= 15:
                    request.session['last_seen_ping'] = now_ts
                    u = request.user
                    if hasattr(u, 'desk_profile'):
                        Desk.objects.filter(pk=u.desk_profile.pk).update(last_seen=now)
                    elif hasattr(u, 'voice_over_profile'):
                        VoiceOverUser.objects.filter(pk=u.voice_over_profile.pk).update(last_seen=now)
                    elif hasattr(u, 'copy_editor_profile'):
                        CopyEditor.objects.filter(pk=u.copy_editor_profile.pk).update(last_seen=now)
                    elif hasattr(u, 'visual_editor_profile'):
                        VisualEditor.objects.filter(pk=u.visual_editor_profile.pk).update(last_seen=now)
                    elif hasattr(u, 'social_media_profile'):
                        SocialMedia.objects.filter(pk=u.social_media_profile.pk).update(last_seen=now)
                    elif hasattr(u, 'reporter_profile'):
                        Reporter.objects.filter(pk=u.reporter_profile.pk).update(last_seen=now)
            except Exception:
                pass

        return self.get_response(request)
