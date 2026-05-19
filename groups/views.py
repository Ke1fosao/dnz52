from django.shortcuts import render, get_object_or_404
from .models import Group


def groups_list(request):
    """Список всіх груп"""
    groups = Group.objects.filter(is_published=True)
    return render(request, 'groups/groups_list.html', {'groups': groups})


def group_detail(request, slug):
    """Сторінка конкретної групи"""
    group = get_object_or_404(Group, slug=slug, is_published=True)
    teachers   = group.get_teachers()
    assistants = group.get_assistants()
    other_groups = Group.objects.filter(is_published=True).exclude(pk=group.pk)
    context = {
        'group':        group,
        'teachers':     teachers,
        'assistants':   assistants,
        'other_groups': other_groups,
    }
    return render(request, 'groups/group_detail.html', context)
