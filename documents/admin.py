from django.contrib import admin
from .models import DocumentCategory, Document

@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at', 'is_published', 'downloads']
    list_filter = ['is_published', 'category', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['downloads', 'created_at']
