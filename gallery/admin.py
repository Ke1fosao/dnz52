from django.contrib import admin
from .models import GalleryAlbum, GalleryPhoto

class GalleryPhotoInline(admin.TabularInline):
    model = GalleryPhoto
    extra = 1

@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'is_published']
    list_filter = ['is_published', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [GalleryPhotoInline]

@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'album', 'order']
    list_filter = ['album']
    list_editable = ['order']
