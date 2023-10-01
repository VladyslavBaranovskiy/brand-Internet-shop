from django.contrib.auth import get_user_model


def full_name(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        return {'full_name': f'{profile.first_name} {profile.last_name}'}
    else:
        return {'full_name': 'Гость'}

def avatar_url(request):
    avatar_url = None

    if request.user.is_authenticated:
        profile = request.user.profile
        avatar_url = profile.avatar.url if profile.avatar else None

    return {'avatar_url': avatar_url}
