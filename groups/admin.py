from django.contrib import admin
from .models import Group, GroupStaff


class GroupStaffInline(admin.TabularInline):
    model = GroupStaff
    extra = 2
    fields = ['role', 'full_name', 'photo', 'birth_date', 'education', 'experience', 'motto', 'order']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display  = ['name', 'age_group', 'order', 'is_published']
    list_editable = ['order', 'is_published']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [GroupStaffInline]
    fieldsets = (
        ('Основне', {
            'fields': ('name', 'slug', 'age_group', 'is_published', 'order')
        }),
        ('Оформлення', {
            'fields': ('cover', 'color', 'motto', 'description')
        }),
        ('Посилання', {
            'fields': ('album',)
        }),
    )


@admin.register(GroupStaff)
class GroupStaffAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'role', 'group']
    list_filter  = ['group', 'role']
