from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Page, PageImage, Slider, Contact,
    ParentsAnnouncement, ParentsDocument, ParentsAdaptationPhoto, ParentsEnrollmentDoc,
    ParentsApplicationSample, StaffMember,
)


class PageImageInline(admin.TabularInline):
    model = PageImage
    extra = 1
    fields = ['image', 'preview', 'caption', 'order', 'is_active']
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px; border-radius:6px;" />',
                obj.image.url,
            )
        return '—'
    preview.short_description = 'Превʼю'


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_published', 'order', 'updated_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['order', 'is_published']
    inlines = [PageImageInline]


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['address', 'phone', 'email']


# ============================================================================
# Адмінка для батьківської сторінки
# ============================================================================

@admin.register(ParentsAnnouncement)
class ParentsAnnouncementAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'preview', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title']

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:60px; border-radius:6px;" />',
                obj.image.url,
            )
        return '—'
    preview.short_description = 'Превʼю'


@admin.register(ParentsDocument)
class ParentsDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'link_type', 'destination', 'icon', 'accent', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['link_type', 'is_active']
    search_fields = ['title', 'description']

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'icon', 'accent', 'order', 'is_active')
        }),
        ('Куди веде', {
            'fields': ('link_type', 'external_url', 'internal_slug', 'file'),
            'description': 'Заповніть лише одне з полів — залежно від обраного типу.'
        }),
    )

    def destination(self, obj):
        url = obj.get_url()
        return format_html('<a href="{0}" target="_blank">{0}</a>', url) if url and url != '#' else '—'
    destination.short_description = 'URL'


@admin.register(ParentsAdaptationPhoto)
class ParentsAdaptationPhotoAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'preview', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title']

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px; border-radius:6px;" />',
                obj.image.url,
            )
        return '—'
    preview.short_description = 'Превʼю'


@admin.register(ParentsEnrollmentDoc)
class ParentsEnrollmentDocAdmin(admin.ModelAdmin):
    list_display = ['title', 'note', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'note']


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', 'preview', 'is_featured', 'order', 'is_active']
    list_editable = ['is_featured', 'order', 'is_active']
    list_filter = ['is_featured', 'is_active']
    search_fields = ['full_name', 'position', 'education', 'awards']

    fieldsets = (
        ('Основна інформація', {
            'fields': ('full_name', 'position', 'photo', 'is_featured', 'accent_color'),
        }),
        ('Кваліфікація', {
            'fields': ('education', 'experience', 'category', 'awards'),
        }),
        ('Біографія', {
            'fields': ('bio',),
            'classes': ('collapse',),
        }),
        ('Контакти', {
            'fields': ('email', 'phone', 'reception_hours'),
        }),
        ('Повна сторінка', {
            'fields': ('detail_url',),
            'description': 'Якщо вказано — на картці зʼявиться кнопка «Повна сторінка», яка веде на вказаний URL (напр. /specialists/psychologist/).',
        }),
        ('Налаштування', {
            'fields': ('order', 'is_active'),
        }),
    )

    def preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="height:60px; width:60px; object-fit:cover; border-radius:50%;" />',
                obj.photo.url,
            )
        return format_html('<span style="color:#888;">— немає фото —</span>')
    preview.short_description = 'Фото'


@admin.register(ParentsApplicationSample)
class ParentsApplicationSampleAdmin(admin.ModelAdmin):
    list_display = ['title', 'preview', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'caption']

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px; border-radius:6px;" />',
                obj.image.url,
            )
        return '—'
    preview.short_description = 'Превʼю'
