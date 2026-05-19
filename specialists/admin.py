from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SpecialistPage, Specialist, SpecialistAlbum,
    SpecialistPageSection, SpecialistPagePhoto,
)


class SpecialistAlbumInline(admin.TabularInline):
    model = SpecialistAlbum
    extra = 1
    fields = ['album', 'description', 'order']


class SpecialistInline(admin.StackedInline):
    model = Specialist
    extra = 1
    fields = ['full_name', 'position', 'photo', 'birth_date',
              'education', 'experience', 'category', 'motto', 'bio', 'order']
    show_change_link = True


class SpecialistPageSectionInline(admin.StackedInline):
    model = SpecialistPageSection
    extra = 0
    fields = ['title', 'kind', 'icon', 'accent', 'order', 'is_active']
    show_change_link = True
    classes = ['collapse']


@admin.register(SpecialistPage)
class SpecialistPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'page_type']
    inlines = [SpecialistInline, SpecialistPageSectionInline]
    fieldsets = (
        ('Основне', {
            'fields': ('page_type', 'title', 'intro'),
        }),
        ('Розширений опис', {
            'fields': ('description',),
            'description': 'Багатий контент, який зʼявляється після карток спеціалістів.',
            'classes': ('collapse',),
        }),
        ('Науково-методична тема', {
            'fields': ('theme_title', 'theme_period', 'theme_text'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', 'page']
    list_filter  = ['page']
    inlines      = [SpecialistAlbumInline]
    fieldsets = (
        ('Основне', {
            'fields': ('page', 'full_name', 'position', 'photo', 'order')
        }),
        ('Особисті дані', {
            'fields': ('birth_date', 'education', 'experience', 'category', 'motto')
        }),
        ('Опис діяльності', {
            'fields': ('bio',)
        }),
    )


class SpecialistPagePhotoInline(admin.TabularInline):
    model = SpecialistPagePhoto
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


@admin.register(SpecialistPageSection)
class SpecialistPageSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'page', 'kind_badge', 'accent', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['page', 'kind', 'is_active']
    search_fields = ['title', 'description']
    inlines = [SpecialistPagePhotoInline]

    fieldsets = (
        ('Основне', {
            'fields': ('page', 'title', 'subtitle', 'description'),
        }),
        ('Зовнішній вигляд', {
            'fields': ('icon', 'accent', 'kind'),
        }),
        ('Для типу «Подія» — посилання', {
            'fields': ('link_album', 'link_news_slug', 'link_external_url', 'link_label'),
            'description': 'Заповніть лише ОДНЕ з полів. Має сенс лише для типу «Подія».',
            'classes': ('collapse',),
        }),
        ('Налаштування', {
            'fields': ('order', 'is_active'),
        }),
    )

    @admin.display(description='Тип', ordering='kind')
    def kind_badge(self, obj):
        if obj.kind == 'event':
            return format_html(
                '<span style="background:#FFB84D; color:#fff; padding:2px 8px; '
                'border-radius:10px; font-size:0.8rem; font-weight:600;">📅 Подія</span>'
            )
        return format_html(
            '<span style="background:#4A90E2; color:#fff; padding:2px 8px; '
            'border-radius:10px; font-size:0.8rem; font-weight:600;">ℹ️ Інформаційна</span>'
        )
