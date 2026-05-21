from django.shortcuts import render, get_object_or_404
from .models import GalleryAlbum, GalleryCategory


def gallery_list(request):
    """Список альбомів, згрупований за категоріями + з фільтром-чіпами угорі."""
    selected_slug = (request.GET.get('cat') or 'all').strip().lower()

    base_qs = GalleryAlbum.objects.filter(is_published=True).select_related('category')
    total_count = base_qs.count()

    # Категорії з підрахунком альбомів — для чіпів-фільтрів
    chips = []
    for cat in GalleryCategory.objects.all():
        count = base_qs.filter(category=cat).count()
        if count > 0:
            chips.append({
                'slug':    cat.slug,
                'name':    cat.name,
                'icon':    cat.icon,
                'color':   cat.color,
                'count':   count,
                'is_active': selected_slug == cat.slug,
            })

    # «Без категорії»
    uncat_count = base_qs.filter(category__isnull=True).count()
    if uncat_count > 0:
        chips.append({
            'slug':    'none',
            'name':    'Без категорії',
            'icon':    'bi-folder-fill',
            'color':   '#7B8AA5',
            'count':   uncat_count,
            'is_active': selected_slug == 'none',
        })

    # Які альбоми показуємо?
    if selected_slug == 'none':
        filtered_qs = base_qs.filter(category__isnull=True)
    elif selected_slug != 'all':
        filtered_qs = base_qs.filter(category__slug=selected_slug)
    else:
        filtered_qs = base_qs

    # Групуємо за категоріями
    grouped = []
    for cat in GalleryCategory.objects.all():
        cat_albums = list(filtered_qs.filter(category=cat))
        if cat_albums:
            grouped.append({'category': cat, 'albums': cat_albums})

    # «Без категорії» в кінці
    uncategorized = list(filtered_qs.filter(category__isnull=True))
    if uncategorized:
        grouped.append({'category': None, 'albums': uncategorized})

    return render(request, 'gallery/gallery_list.html', {
        'grouped':       grouped,
        'chips':         chips,
        'selected_slug': selected_slug,
        'total_count':   total_count,
        'showing_count': filtered_qs.count(),
    })


def album_detail(request, slug):
    """Фото в альбомі"""
    album = get_object_or_404(GalleryAlbum, slug=slug, is_published=True)
    photos = album.photos.all()
    return render(request, 'gallery/album_detail.html', {'album': album, 'photos': photos})
