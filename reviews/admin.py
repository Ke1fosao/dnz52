from django.contrib import admin
from django.utils.html import format_html
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'author', 'child_group', 'stars_visual', 'created_at_short',
        'short_text', 'is_approved',
    ]
    list_editable = ['is_approved']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['author', 'child_group', 'text']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    list_per_page = 25

    fieldsets = (
        ('Інформація про автора', {
            'fields': ('author', 'child_group'),
        }),
        ('Відгук', {
            'fields': ('rating', 'text'),
        }),
        ('Модерація', {
            'fields': ('is_approved', 'created_at'),
        }),
    )

    actions = ['approve_selected', 'unapprove_selected']

    @admin.display(description='Оцінка', ordering='rating')
    def stars_visual(self, obj):
        filled = '★' * obj.rating
        empty = '☆' * (5 - obj.rating)
        return format_html(
            '<span style="color:#FFB000; font-size:1.05rem; letter-spacing:1px;">{}</span>'
            '<span style="color:#CCC; font-size:1.05rem; letter-spacing:1px;">{}</span>'
            '<span style="color:#888; font-size:0.8rem; margin-left:6px;">({}/5)</span>',
            filled, empty, obj.rating,
        )

    @admin.display(description='Дата', ordering='created_at')
    def created_at_short(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M')

    @admin.display(description='Текст відгуку')
    def short_text(self, obj):
        text = obj.text
        if len(text) > 80:
            text = text[:77] + '…'
        return text

    @admin.action(description='✓ Опублікувати вибрані відгуки')
    def approve_selected(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'Опубліковано: {updated} відгук(ів).')

    @admin.action(description='✗ Зняти з публікації вибрані відгуки')
    def unapprove_selected(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'Знято з публікації: {updated} відгук(ів).')
