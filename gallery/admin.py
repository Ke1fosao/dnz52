from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryAlbum, GalleryPhoto, GalleryCategory


class GalleryPhotoInline(admin.TabularInline):
    model = GalleryPhoto
    extra = 1
    fields = ['image', 'preview', 'title', 'order']
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" style="max-height:64px; border-radius:6px;" />',
                obj.image.url,
            )
        return '—'
    preview.short_description = 'Превʼю'


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_chip', 'icon', 'albums_count', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Основне', {
            'fields': ('name', 'slug', 'order'),
        }),
        ('Вигляд', {
            'fields': ('icon', 'color'),
            'description': 'Іконка з Bootstrap Icons (https://icons.getbootstrap.com/) '
                            'і колір заголовка секції у галереї.'
        }),
    )

    def color_chip(self, obj):
        return format_html(
            '<span style="display:inline-block; width:20px; height:20px; vertical-align:middle; '
            'border-radius:6px; background:{0}; border:1px solid rgba(0,0,0,0.1);"></span>'
            '<span style="margin-left:8px; font-family:monospace;">{0}</span>',
            obj.color,
        )
    color_chip.short_description = 'Колір'

    def albums_count(self, obj):
        return obj.albums.count()
    albums_count.short_description = 'Альбомів'


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_chip', 'photos_count', 'created_at', 'is_published']
    list_filter = ['category', 'is_published', 'created_at']
    list_editable = ['is_published']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [GalleryPhotoInline]

    fieldsets = (
        ('Основне', {
            'fields': ('title', 'slug', 'category', 'cover', 'description'),
        }),
        ('Налаштування', {
            'fields': ('is_published',),
        }),
    )

    def category_chip(self, obj):
        if not obj.category:
            return format_html('<span style="color:#aaa;">— Без категорії —</span>')
        return format_html(
            '<span style="display:inline-block; padding:3px 12px; border-radius:12px; '
            'background:{0}22; color:{0}; font-weight:600; font-size:0.78rem;">{1}</span>',
            obj.category.color, obj.category.name,
        )
    category_chip.short_description = 'Категорія'

    def photos_count(self, obj):
        return obj.photos.count()
    photos_count.short_description = 'Фото'


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'album', 'preview', 'order']
    list_filter = ['album']
    list_editable = ['order']
    search_fields = ['title', 'album__title']

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:48px; border-radius:4px;" />',
                obj.image.url,
            )
        return '—'
    preview.short_description = 'Превʼю'
