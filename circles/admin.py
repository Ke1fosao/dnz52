from django.contrib import admin
from .models import Circle, CircleDocument


@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    list_display  = ['name', 'leader', 'age_group', 'order', 'is_published']
    list_editable = ['order', 'is_published']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Основне', {'fields': ('name', 'slug', 'is_published', 'order', 'icon', 'color')}),
        ('Інформація', {'fields': ('leader', 'age_group', 'schedule')}),
        ('Контент', {'fields': ('goal', 'description')}),
        ('Альбом', {'fields': ('album',)}),
    )


@admin.register(CircleDocument)
class CircleDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'document', 'order']
    list_editable = ['order']
