from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Page, PageImage, Slider, Contact,
    ParentsAnnouncement, ParentsDocument, ParentsAdaptationPhoto, ParentsEnrollmentDoc,
    ParentsApplicationSample, StaffMember,
    AttestationDocument, AttestationStep, AttestationCategory, AttestationLaw,
    AttestationSettings,
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


# ============================================================================
# Адмінка для сторінки «Атестація»
# ============================================================================

@admin.register(AttestationSettings)
class AttestationSettingsAdmin(admin.ModelAdmin):
    """Єдиний запис налаштувань — не дозволяємо створювати нові копії або видаляти."""
    fieldsets = (
        ('Hero (верхня частина)', {
            'fields': ('hero_lead',),
            'description': 'Текст під заголовком «Атестація педагогічних працівників».'
        }),
        ('Вступний синій блок', {
            'fields': ('intro_html',),
        }),
        ('Секція документів', {
            'fields': ('docs_section_subtitle',),
            'description': 'Підзаголовок під назвою «Документи атестаційної комісії».'
        }),
        ('Жовта плашка з контактами', {
            'fields': ('contact_title', 'contact_html'),
            'description': 'Блок «Маєте запитання?» унизу сторінки.'
        }),
    )

    def has_add_permission(self, request):
        return not AttestationSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        """Якщо ще немає запису — створюємо порожній, щоб одразу відкрити його редагування."""
        obj = AttestationSettings.get_solo()
        from django.shortcuts import redirect
        from django.urls import reverse
        return redirect(reverse('admin:main_attestationsettings_change', args=[obj.pk]))


@admin.register(AttestationDocument)
class AttestationDocumentAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'category', 'accent_chip', 'url_link', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active', 'category']
    search_fields = ['title', 'subtitle']

    fieldsets = (
        ('Основне', {
            'fields': ('title', 'subtitle', 'category', 'url'),
        }),
        ('Вигляд', {
            'fields': ('icon', 'accent'),
            'description': 'Іконка з Bootstrap Icons (https://icons.getbootstrap.com/). '
                            'Колір впливає на смужку зліва на картці.'
        }),
        ('Порядок', {
            'fields': ('order', 'is_active'),
        }),
    )

    def accent_chip(self, obj):
        colors = {
            'primary': '#4A90E2', 'success': '#34C8A8', 'warning': '#FF9F1A',
            'info': '#2DA0BB', 'purple': '#7C4DCB', 'danger': '#E5677E',
        }
        c = colors.get(obj.accent, '#888')
        return format_html(
            '<span style="display:inline-block; padding:3px 10px; border-radius:12px; '
            'background:{0}; color:#fff; font-size:0.78rem; font-weight:600;">{1}</span>',
            c, obj.get_accent_display()
        )
    accent_chip.short_description = 'Колір'

    def url_link(self, obj):
        if not obj.url:
            return '—'
        return format_html('<a href="{0}" target="_blank">Відкрити ↗</a>', obj.url)
    url_link.short_description = 'Посилання'


@admin.register(AttestationStep)
class AttestationStepAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'order', 'is_active'),
            'description': 'Поле «Порядок» = номер кроку у списку. Менше число — раніше.'
        }),
    )


@admin.register(AttestationCategory)
class AttestationCategoryAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'color_chip', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active', 'color']
    search_fields = ['title', 'description']

    fieldsets = (
        ('Основне', {
            'fields': ('title', 'description'),
        }),
        ('Вигляд', {
            'fields': ('icon', 'color'),
        }),
        ('Порядок', {
            'fields': ('order', 'is_active'),
        }),
    )

    def color_chip(self, obj):
        gradients = {
            'cat-1': 'linear-gradient(135deg, #50E3C2, #34C8A8)',
            'cat-2': 'linear-gradient(135deg, #38C2DD, #2DA0BB)',
            'cat-3': 'linear-gradient(135deg, #4A90E2, #357ABD)',
            'cat-4': 'linear-gradient(135deg, #B388FF, #7C4DCB)',
        }
        g = gradients.get(obj.color, '#888')
        return format_html(
            '<span style="display:inline-block; padding:3px 12px; border-radius:12px; '
            'background:{0}; color:#fff; font-size:0.78rem; font-weight:600;">{1}</span>',
            g, obj.get_color_display()
        )
    color_chip.short_description = 'Колір'


@admin.register(AttestationLaw)
class AttestationLawAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'has_link', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['title']

    def has_link(self, obj):
        if obj.url:
            return format_html('<a href="{0}" target="_blank">Відкрити ↗</a>', obj.url)
        return '—'
    has_link.short_description = 'Посилання'


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
