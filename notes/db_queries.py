import re

from bleach import clean
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Q

from notes.models import Note, Tag, UserProfile

CACHE_PERIOD = 60 * 60


def get_list(request):
    tag = request.GET.get('tag')
    q = request.GET.get('q')
    user = request.GET.get('user')
    query = Q(deleted=False)

    if not request.user.is_authenticated:
        query &= Q(private=False)
    else:
        query &= Q(private=False) | (Q(user_id=request.user.id) & Q(private=True))
    if tag:
        query &= Q(tag__tag=tag)

    if q:
        query &= (Q(title__icontains=q) | Q(body__icontains=q))

    if user:
        query &= Q(user__id=user)

    notes_cache = cache.get(query)
    if notes_cache:
        notes = notes_cache
    else:
        notes = Note.objects.filter(query).prefetch_related('user__userprofile').all()
        cache.set(query, notes, CACHE_PERIOD)
    for note in notes:
        note.tags = get_tags_by_note_id(note.id)
        note.body = clean(note.body, tags=['br', 'p', 'hr', 'a'])
        note.body = replace_urls_with_links(note.body[:200].replace('\n', '<br />'))
        avatar = note.user.userprofile.avatar
        note.avatar = avatar
    return notes


def get_note_by_id(note_id):
    cache_key = {'note': note_id}
    note = cache.get(cache_key)
    if note is None:
        note = Note.objects.get(id=note_id)
        cache.set(cache_key, note, CACHE_PERIOD)
    return note


def get_tags_by_substring(substr: str):
    list_tags = Tag.objects.filter(Q(tag__icontains=substr))
    return list_tags


def get_tags_by_note_id(note_id: int):
    cache_key = f'tags_{note_id}'
    tags_list = cache.get(cache_key)
    if tags_list is None:
        tags_list = Tag.objects.filter(note_id=note_id)
        cache.set(cache_key, tags_list, CACHE_PERIOD)
    return tags_list


def create_tag(tag: str, note_id: Note):
    Tag.objects.create(tag=tag, note_id=note_id)
    cache.delete(f'tags_{note_id.id}')


def replace_urls_with_links(text):
    # Регулярное выражение для поиска URL
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    # Функция для замены URL на теги <a href...>
    def replace_url(match):
        url = match.group(0)
        return f'<a href="{url}">{url}</a>'

    # Замена URL на теги <a href...>
    replaced_text = re.sub(url_pattern, replace_url, text)
    return replaced_text


def get_user_profile(user: User):
    cache_key = {'user_profile': user.id}
    user_profile = cache.get(cache_key)
    if user_profile is None:
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            user_profile = None
        cache.set(cache_key, user_profile, CACHE_PERIOD)
    return user_profile
