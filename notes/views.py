import logging
from datetime import datetime

from bleach import clean
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from django_notes.settings import BASE_DIR
from notes.db_queries import (create_tag, get_list, get_note_by_id,
                              get_tags_by_note_id, get_tags_by_substring)
from notes.forms import NoteModelForm
from notes.models import Note, Tag
from notes.Shares import Shares


def set_logger():
    logging.basicConfig(filename=f'{BASE_DIR}/logs/debug.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


# def get_list(request):
#     """
#     Ищет и возвращает список объектов Note
#     :param request: q = подстрока запроса
#     :return:
#     """
#     condition_not_deleted = Q(deleted=False)
#     condition = condition_not_deleted
#     # Поиск по подстроке
#     if request.GET.get('q') is not None:
#         condition = condition_not_deleted & \
#                     (Q(title__icontains=request.GET.get('q')) | Q(body__icontains=request.GET.get('q')))
#
#     # Поиск по тегу
#     if request.GET.get('tag'):
#         condition = condition & Q(tag__tag=request.GET.get('tag'))
#
#     # Только заметки пользователя
#     if request.GET.get('user'):
#         condition = condition & Q(user__id=request.GET.get('user'))
#         if request.user.is_authenticated and request.user.id == int(request.GET.get('user')):
#             print(f'Filter without private: user.id:{request.user.id} get: {request.GET.get("user")}')
#             notes = Note.objects.filter(
#                 condition
#             ).prefetch_related('user__userprofile')
#         else:
#             print(f'Filter with private: user.id:{request.user.id} get: {request.GET.get("user")}')
#             notes = Note.objects.filter(Q(private=False) & condition).prefetch_related('user__userprofile').all()
#     else:
#         notes = Note.objects.filter(Q(private=False) & condition).prefetch_related('user__userprofile').all()
#     for note in notes:
#         note.tags = Tag.objects.filter(note_id=note.id)
#         note.body = clean(note.body, tags=['br', 'p', 'hr', 'a'])
#         note.body = replace_urls_with_links(note.body[:200].replace('\n', '<br />'))
#         avatar = note.user.userprofile.avatar
#         note.avatar = avatar
#     return notes


def paginate_notes(notes, page_number):
    paginator = Paginator(notes, 20)
    return paginator.get_page(page_number)


def index(request):
    """
    Shows main page with list of notes
    """
    set_logger()
    logger = logging.getLogger(__name__)
    logger.debug("vew.index")
    if request.user.is_authenticated:
        add_shared(request)
    notes = paginate_notes(get_list(request), request.GET.get('page'))
    return render(request, 'notes/index.html', {'notes': notes})


def add_shared(request):
    """
    Calls Shares class for add shared notes
    """
    shares = Shares(request.user)
    shares.process()


@login_required
def new(request):
    """
    Shows form to create new note
    :param request:
    """
    user = request.user
    if request.method == 'POST':
        note_form = NoteModelForm(request.POST, request.FILES)
        if note_form.is_valid():
            note_obj = note_form.save(commit=False)
            note_obj.user = user
            note_obj.save()
            for i in range(0, 100):
                if request.POST.get(f'tag{i}') is not None:
                    tag = Tag()
                    tag.tag = request.POST.get(f'tag{i}')
                    tag.note_id = note_obj
                    tag.save()
                else:
                    break
            return redirect('index')
    else:
        if user.is_authenticated:
            note_form = NoteModelForm()
            context = {'note_form': note_form, 'js_tags': '[]'}
            return render(request, 'notes/edit.html', context)
        else:
            return redirect('index')


def tags(request):
    """
    Generates JSON list of tags
    :param request: q - string to search
    :return: JSON response
    """
    q = request.GET.get('q')
    list_tags = get_tags_by_substring(q)
    result = {}
    if list_tags is None:
        return JsonResponse(result)
    for tag in list_tags:
        result[tag.tag] = f'{tag.tag}'
    return JsonResponse(result)


def show(request, note_id):
    """
    Shows note with template notes/show.html
    """
    note = get_object_or_404(Note, pk=note_id)
    note.tags = get_tags_by_note_id(note_id=note.id)
    note.body = clean(note.body, tags=['br', 'p', 'hr'])
    note.body = note.body.replace('\n', '<br />')
    return render(request, 'notes/show.html', {'note': note})


def list_notes(request):
    """
    Возвращает render списка объектов Note
    :param request:
    :return:
    """
    notes = paginate_notes(get_list(request), request.GET.get('page'))
    return render(request, 'notes/list.html', {'notes': notes})


# @login_required()


@login_required
def edit(request, note_id):
    debug = True
    note = get_object_or_404(Note, pk=note_id)
    user = request.user
    if request.method == 'POST' and note.user_id == user.id:
        note_form = NoteModelForm(request.POST, instance=note)
        # tag_forms = [TagModelForm(request.POST, prefix=str(i), instance=tag) for i, tag in enumerate(note.tags.all())]
        if note_form.is_valid():
            note_obj = note_form.save(commit=False)
            note_obj.user = user
            note_obj.save()
            # получаем sets имеющихся и новых тегов
            new_tags = set([value for key, value in request.POST.items() if key.startswith('tag')])
            old_tags = set([str(tag) for tag in get_tags_by_note_id(note_id=note.id)])
            # Генерим новые сеты для удаления и добавления
            tags_to_delete = old_tags - new_tags
            tags_to_add = new_tags - old_tags
            if debug:
                print(f'old_tags: {list(old_tags)}')
                print(f'new_tags: {list(new_tags)}')
                print(f'tags_to_delete: {list(tags_to_delete)}')
                print(f'tags_to_add: {list(tags_to_add)}')
            Tag.objects.filter(note_id=note.id, tag__in=tags_to_delete).delete()
            for tag in tags_to_add:
                note = get_note_by_id(note_id=note_id)
                create_tag(tag=tag, note_id=note)
            return redirect('note_show', note_id=note_id)

        pass
    else:
        if note.user_id == user.id:
            note_form = NoteModelForm(instance=note)
            note.tags = get_tags_by_note_id(note_id=note.id)
            js_tags = [f'"{tag}"' for tag in note.tags]
            js_tags = '[' + ', '.join(js_tags) + ']'
            context = {'note_form': note_form, 'js_tags': js_tags}
            return render(request, 'notes/edit.html', context)
    return redirect('note_show', note_id=note_id)


@login_required
def delete(request, note_id):
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=note_id)
        if note.user_id == request.user.id:
            note.deleted = True
            note.deleted_at = datetime.now()
            note.save()
        return redirect('index')
