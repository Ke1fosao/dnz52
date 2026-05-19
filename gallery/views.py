from django.shortcuts import render, get_object_or_404
from .models import GalleryAlbum

def gallery_list(request):
    """Список альбомів"""
    albums = GalleryAlbum.objects.filter(is_published=True)
    return render(request, 'gallery/gallery_list.html', {'albums': albums})

def album_detail(request, slug):
    """Фото в альбомі"""
    album = get_object_or_404(GalleryAlbum, slug=slug, is_published=True)
    photos = album.photos.all()
    return render(request, 'gallery/album_detail.html', {'album': album, 'photos': photos})
