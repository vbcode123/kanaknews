from django.utils import timezone
from .models import Desk, VoiceOverUser, CopyEditor, VisualEditor, SocialMedia, Reporter


def touch_user_last_seen(u, now=None):
    """
    Safely updates last_seen for the currently authenticated user's own profile.
    Only touches profiles directly linked to this authenticated user account.
    """
    if not u or not getattr(u, 'is_authenticated', False):
        return
    if now is None:
        now = timezone.now()

    try:
        rep = getattr(u, 'reporter_profile', None)
        if rep:
            Reporter.objects.filter(pk=rep.pk).update(last_seen=now)
    except Exception:
        pass

    try:
        desk = getattr(u, 'desk_profile', None)
        if desk:
            Desk.objects.filter(pk=desk.pk).update(last_seen=now)
    except Exception:
        pass

    try:
        sm = getattr(u, 'social_media_profile', None)
        if sm:
            SocialMedia.objects.filter(pk=sm.pk).update(last_seen=now)
    except Exception:
        pass

    try:
        ve = getattr(u, 'visual_editor_profile', None)
        if ve:
            VisualEditor.objects.filter(pk=ve.pk).update(last_seen=now)
    except Exception:
        pass

    try:
        ce = getattr(u, 'copy_editor_profile', None)
        if ce:
            CopyEditor.objects.filter(pk=ce.pk).update(last_seen=now)
    except Exception:
        pass

    try:
        vo = getattr(u, 'voice_over_profile', None)
        if vo:
            VoiceOverUser.objects.filter(pk=vo.pk).update(last_seen=now)
    except Exception:
        pass

    try:
        gd = getattr(u, 'graphic_designer_profile', None)
        if gd:
            from .models import GraphicDesigner
            GraphicDesigner.objects.filter(pk=gd.pk).update(last_seen=now)
    except Exception:
        pass

    try:
        inp = getattr(u, 'input_profile', None)
        if inp:
            from .models import InputUser
            InputUser.objects.filter(pk=inp.pk).update(last_seen=now)
    except Exception:
        pass


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
                    touch_user_last_seen(request.user, now)
            except Exception:
                pass

        return self.get_response(request)
