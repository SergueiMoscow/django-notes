from notes.models import UserProfile


def avatar_context_processor(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            profile = None
        return {'avatar': profile.avatar if profile else None}
    else:
        return {}
