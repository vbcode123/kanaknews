from django.utils import timezone
from .models import (
    DeskVisualChatMessage, DeskCopyChatMessage, DeskVoiceOverChatMessage, 
    DeskSocialChatMessage, DeskReporterChatMessage, MediaDownloadRequest
)


def chat_unread_counts(request):
    """
    Context processor to provide real-time unread chat badge counts
    for Desk, Visual Editor, Copy Editor, Voice Over, Social Media, and Reporter portals,
    and pending download approvals count for Admin.
    """
    context = {
        'desk_unread_chat_count': 0,
        'desk_unread_copy_chat_count': 0,
        'desk_unread_vo_chat_count': 0,
        'desk_unread_social_chat_count': 0,
        'desk_unread_reporter_chat_count': 0,
        've_unread_chat_count': 0,
        'ce_unread_chat_count': 0,
        'vo_unread_chat_count': 0,
        'sm_unread_chat_count': 0,
        'social_unread_chat_count': 0,
        'reporter_unread_chat_count': 0,
        'pending_download_approvals_count': 0,
        'is_exempt_from_download_guard': False,
        'current_user_role': 'unknown',
    }

    if not hasattr(request, 'user') or not request.user.is_authenticated:
        return context

    try:
        # Check if user is Admin or Input (Exempt from download approvals)
        if request.user.is_superuser or (request.user.is_staff and not any(hasattr(request.user, p) for p in [
            'desk_profile', 'visual_editor_profile', 'copy_editor_profile', 'voice_over_profile',
            'social_media_profile', 'graphic_designer_profile', 'reporter_profile', 'input_profile'
        ])):
            context['is_exempt_from_download_guard'] = True
            context['current_user_role'] = 'admin'
            # Count pending download requests for admin
            try:
                context['pending_download_approvals_count'] = MediaDownloadRequest.objects.filter(
                    is_approved=False,
                    is_used=False,
                    is_rejected=False,
                    expires_at__gt=timezone.now()
                ).count()
            except Exception:
                context['pending_download_approvals_count'] = 0

        elif hasattr(request.user, 'input_profile'):
            context['is_exempt_from_download_guard'] = True
            context['current_user_role'] = 'input'

        elif hasattr(request.user, 'desk_profile'):
            context['current_user_role'] = 'desk'
            desk = request.user.desk_profile
            context['desk_unread_chat_count'] = DeskVisualChatMessage.objects.filter(
                desk=desk,
                sender_type='visual_editor',
                is_read=False
            ).count()
            context['desk_unread_copy_chat_count'] = DeskCopyChatMessage.objects.filter(
                desk=desk,
                sender_type='copy_editor',
                is_read=False
            ).count()
            context['desk_unread_vo_chat_count'] = DeskVoiceOverChatMessage.objects.filter(
                desk=desk,
                sender_type='voice_over',
                is_read=False
            ).count()
            context['desk_unread_social_chat_count'] = DeskSocialChatMessage.objects.filter(
                desk=desk,
                sender_type='social_media',
                is_read=False
            ).count()
            context['desk_unread_reporter_chat_count'] = DeskReporterChatMessage.objects.filter(
                desk=desk,
                sender_type='reporter',
                is_read=False
            ).count()
        elif hasattr(request.user, 'visual_editor_profile'):
            context['current_user_role'] = 'visual_editor'
            ve = request.user.visual_editor_profile
            context['ve_unread_chat_count'] = DeskVisualChatMessage.objects.filter(
                visual_editor=ve,
                sender_type='desk',
                is_read=False
            ).count()
        elif hasattr(request.user, 'copy_editor_profile'):
            context['current_user_role'] = 'copy_editor'
            ce = request.user.copy_editor_profile
            context['ce_unread_chat_count'] = DeskCopyChatMessage.objects.filter(
                copy_editor=ce,
                sender_type='desk',
                is_read=False
            ).count()
        elif hasattr(request.user, 'voice_over_profile'):
            context['current_user_role'] = 'voice_over'
            vo = request.user.voice_over_profile
            context['vo_unread_chat_count'] = DeskVoiceOverChatMessage.objects.filter(
                voice_over=vo,
                sender_type='desk',
                is_read=False
            ).count()
        elif hasattr(request.user, 'social_media_profile'):
            context['current_user_role'] = 'social_media'
            sm = request.user.social_media_profile
            count = DeskSocialChatMessage.objects.filter(
                social_media=sm,
                sender_type='desk',
                is_read=False
            ).count()
            context['sm_unread_chat_count'] = count
            context['social_unread_chat_count'] = count
        elif hasattr(request.user, 'graphic_designer_profile'):
            context['current_user_role'] = 'graphic_designer'
        elif hasattr(request.user, 'reporter_profile'):
            context['current_user_role'] = 'reporter'
            rep = request.user.reporter_profile
            context['reporter_unread_chat_count'] = DeskReporterChatMessage.objects.filter(
                reporter=rep,
                sender_type='desk',
                is_read=False
            ).count()
    except Exception:
        pass

    return context
