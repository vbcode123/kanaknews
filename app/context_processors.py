from .models import DeskVisualChatMessage, DeskCopyChatMessage, DeskVoiceOverChatMessage, DeskSocialChatMessage, DeskReporterChatMessage


def chat_unread_counts(request):
    """
    Context processor to provide real-time unread chat badge counts
    for Desk, Visual Editor, Copy Editor, Voice Hover, Social Media, and Reporter portals across all pages.
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
    }

    if not hasattr(request, 'user') or not request.user.is_authenticated:
        return context

    try:
        if hasattr(request.user, 'desk_profile'):
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
            ve = request.user.visual_editor_profile
            context['ve_unread_chat_count'] = DeskVisualChatMessage.objects.filter(
                visual_editor=ve,
                sender_type='desk',
                is_read=False
            ).count()
        elif hasattr(request.user, 'copy_editor_profile'):
            ce = request.user.copy_editor_profile
            context['ce_unread_chat_count'] = DeskCopyChatMessage.objects.filter(
                copy_editor=ce,
                sender_type='desk',
                is_read=False
            ).count()
        elif hasattr(request.user, 'voice_over_profile'):
            vo = request.user.voice_over_profile
            context['vo_unread_chat_count'] = DeskVoiceOverChatMessage.objects.filter(
                voice_over=vo,
                sender_type='desk',
                is_read=False
            ).count()
        elif hasattr(request.user, 'social_media_profile'):
            sm = request.user.social_media_profile
            count = DeskSocialChatMessage.objects.filter(
                social_media=sm,
                sender_type='desk',
                is_read=False
            ).count()
            context['sm_unread_chat_count'] = count
            context['social_unread_chat_count'] = count
        elif hasattr(request.user, 'reporter_profile'):
            rep = request.user.reporter_profile
            context['reporter_unread_chat_count'] = DeskReporterChatMessage.objects.filter(
                reporter=rep,
                sender_type='desk',
                is_read=False
            ).count()
    except Exception:
        pass

    return context
