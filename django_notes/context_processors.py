from notes.db_queries import get_user_profile


def avatar_context_processor(request):
    if request.user.is_authenticated:
        profile = get_user_profile(user=request.user)
        return {'avatar': profile.avatar if profile else None}
    else:
        return {}
