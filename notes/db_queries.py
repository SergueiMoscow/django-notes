import re

from bleach import clean
from django.contrib.auth.models import User
from django.db.models import Q

from notes.models import Note, Tag, UserProfile


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

    notes = Note.objects.filter(query).prefetch_related('user__userprofile').all()

    for note in notes:
        note.tags = get_tags_by_note_id(note.id)
        note.body = clean(note.body, tags=['br', 'p', 'hr', 'a'])
        note.body = replace_urls_with_links(note.body[:200])
        note.body = note.body.replace('\n', '<br />')
        avatar = note.user.userprofile.avatar
        note.avatar = avatar
    return notes


def generate_cash_key(key: dict):
    pass


def get_note_by_id(note_id):
    note = Note.objects.get(id=note_id)
    return note


def get_tags_by_substring(substr: str):
    list_tags = Tag.objects.filter(Q(tag__icontains=substr))
    return list_tags


def get_tags_by_note_id(note_id: int):
    tags_list = Tag.objects.filter(note_id=note_id)
    return tags_list


def create_tag(tag: str, note_id: Note):
    Tag.objects.create(tag=tag, note_id=note_id)


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
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None
    return user_profile
