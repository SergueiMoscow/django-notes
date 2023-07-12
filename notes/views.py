from django.db.models import Q
from django.shortcuts import render, redirect

from notes.forms import NoteModelForm, TagModelForm
from notes.models import Tag, Note
from django.http import JsonResponse


def index(request):
    return render(request, 'notes/index.html')


def new(request):
    user = request.user
    if request.method == 'POST':
        note_form = NoteModelForm(request.POST)
        tag_forms = [TagModelForm(request.POST, prefix=str(i)) for i in range(1, len(request.POST))]
        if note_form.is_valid() and all(tag_form.is_valid() for tag_form in tag_forms):
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
            return redirect('index')
    else:
        note_form = NoteModelForm()
        tag_forms = [TagModelForm(prefix=str(i)) for i in range(1, 6)]

        context = {'note_form': note_form, 'tag_forms': tag_forms}
        return render(request, 'notes/new.html', context)


def tags(request):
    q = request.GET.get('q')
    list_tags = Tag.objects.filter(Q(tag__icontains=q))
    result = {}
    if list_tags is None:
        return JsonResponse(result)
    for tag in list_tags:
        result[tag.tag] = f'{tag.tag}'
    return JsonResponse(result)
