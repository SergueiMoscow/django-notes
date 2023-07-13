from datetime import datetime

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from notes.forms import NoteModelForm, TagModelForm
from notes.models import Tag, Note
from django.http import JsonResponse


def get_list(request):
    """
    Ищет и возвращает список объектов Note
    :param request: q = подстрока запроса
    :return:
    """
    condition_not_deleted = Q(deleted=False)
    condition = condition_not_deleted
    if request.GET.get('q') is not None:
        condition = condition_not_deleted & \
                    (Q(title__icontains=request.GET.get('q')) | Q(body__icontains=request.GET.get('q')))

    if request.user.is_authenticated:
        notes = Note.objects.filter(
            user=request.user and
            condition and
            Q(deleted=False)
        )
    else:
        notes = Note.objects.filter(Q(private=False) & condition).all()
    for note in notes:
        note.tags = Tag.objects.filter(note_id=note.id)
    return notes


def index(request):
    """
    Shows main page with list of notes
    """
    notes = get_list(request)
    return render(request, 'notes/index.html', {'notes': notes})


def new(request):
    """
    Shows form to create new note
    :param request:
    """
    user = request.user
    if request.method == 'POST':
        note_form = NoteModelForm(request.POST, request.FILES)
        if note_form.is_valid():
            print(f'Post: {request.POST}, Files: {request.FILES}')
            note_obj = note_form.save(commit=False)
            note_obj.user = user
            note_obj.save()
            print(f'Note saved: {note_obj}')
            tag = request.POST.get('tag1')
            print(f'tag: {tag}')
            for i in range(0, 100):
                if request.POST.get(f'tag{i}') is not None:
                    tag = Tag()
                    tag.tag = request.POST.get(f'tag{i}')
                    tag.note_id = note_obj
                    print(f'tag: {tag}')
                    tag.save()
                else:
                    break;
            return redirect('index')
    else:
        note_form = NoteModelForm()
        context = {'note_form': note_form, 'js_tags': '[]'}
        return render(request, 'notes/new.html', context)


def tags(request):
    """
    Generates JSON list of tags
    :param request: q - string to search
    :return: JSON response
    """
    q = request.GET.get('q')
    list_tags = Tag.objects.filter(Q(tag__icontains=q))
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
    note.tags = Tag.objects.filter(note_id=note.id)
    return render(request, 'notes/show.html', {'note': note})


def list_notes(request):
    """
    Возвращает render списка объектов Note
    :param request:
    :return:
    """
    notes = get_list(request)
    return render(request, 'notes/list.html', {'notes': notes})


def edit(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    user = request.user
    if request.method == 'POST':
        note_form = NoteModelForm(request.POST, instance=note)
        tag_forms = [TagModelForm(request.POST, prefix=str(i), instance=tag) for i, tag in enumerate(note.tags.all())]
        if note_form.is_valid():
            print(f'Post: {request.POST}')
            note_obj = note_form.save(commit=False)
            note_obj.user = user
            note_obj.save()
            print(f'Note saved: {note_obj}')
            tag = request.POST.get('tag1')
            print(f'tag: {tag}')
            for i in range(0, 100):
                if request.POST.get(f'tag{i}') is not None:
                    tag = Tag()
                    tag.tag = request.POST.get(f'tag{i}')
                    tag.note_id = note_obj
                    print(f'tag: {tag}')
                    tag.save()
                else:
                    break;
            return redirect('note_show', note_id=note_id)

        pass
    else:
        note_form = NoteModelForm(instance=note)
        # tag_forms = [TagModelForm(instance=tag, prefix=str(i)) for i, tag in enumerate(note.tags.all())]
        note.tags = Tag.objects.filter(note_id=note.id)
        js_tags = [f'"{tag}"' for tag in note.tags]
        js_tags = '[' + ', '.join(js_tags) + ']'
        context = {'note_form': note_form, 'js_tags': js_tags}
        return render(request, 'notes/new.html', context)
    return redirect('note_show', note_id=note_id)


def delete(request, note_id):
    print(f'Request: {request}')
    print(f'note_id: {note_id}')
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=note_id)
        note.deleted = True
        note.deleted_at = datetime.now()
        note.save()
        return redirect('index')
