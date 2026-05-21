from datetime import timedelta
from django.contrib import admin, messages
from django.utils.html import format_html
from .models import DailyMenu


_WEEKDAYS_UK = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', "П'ятниця", 'Субота', 'Неділя']


@admin.register(DailyMenu)
class DailyMenuAdmin(admin.ModelAdmin):
    list_display = ['date_display', 'weekday', 'meals_chips', 'note', 'is_published']
    list_editable = ['is_published']
    list_filter = ['is_published']
    search_fields = ['breakfast', 'second_breakfast', 'lunch', 'snack', 'dinner', 'note']
    ordering = ['-date']
    save_on_top = True
    list_per_page = 30

    fieldsets = (
        ('🗓️ День', {
            'fields': ('date', 'note', 'is_published'),
            'description': 'Виберіть дату. Якщо в день не передбачено якогось прийому їжі — '
                            'просто залиште поле порожнім.'
        }),
        ('🥣 Сніданок', {
            'fields': ('breakfast', 'second_breakfast'),
        }),
        ('🍲 Обід', {
            'fields': ('lunch',),
        }),
        ('🥨 Полуденок та вечеря', {
            'fields': ('snack', 'dinner'),
        }),
    )

    actions = ['duplicate_to_next_week']

    def date_display(self, obj):
        return obj.date.strftime('%d.%m.%Y')
    date_display.short_description = 'Дата'
    date_display.admin_order_field = 'date'

    def weekday(self, obj):
        return _WEEKDAYS_UK[obj.date.weekday()]
    weekday.short_description = 'День тижня'

    def meals_chips(self, obj):
        chips = []
        for emoji, value in [('🥣', obj.breakfast), ('🍎', obj.second_breakfast),
                              ('🍲', obj.lunch), ('🥨', obj.snack), ('🥛', obj.dinner)]:
            if value:
                chips.append(emoji)
        if not chips:
            return format_html('<span style="color:#aaa;">— порожньо —</span>')
        return ' '.join(chips)
    meals_chips.short_description = 'Прийоми їжі'

    @admin.action(description='📋 Скопіювати вибрані дні на наступний тиждень')
    def duplicate_to_next_week(self, request, queryset):
        """Створює копії вибраних меню зі зсувом +7 днів. Якщо запис на ту дату вже існує — пропускає."""
        created = 0
        skipped = 0
        for original in queryset:
            new_date = original.date + timedelta(days=7)
            if DailyMenu.objects.filter(date=new_date).exists():
                skipped += 1
                continue
            DailyMenu.objects.create(
                date=new_date,
                breakfast=original.breakfast,
                second_breakfast=original.second_breakfast,
                lunch=original.lunch,
                snack=original.snack,
                dinner=original.dinner,
                note=original.note,
                is_published=original.is_published,
            )
            created += 1
        if created:
            messages.success(
                request,
                f'Створено {created} нових записів на наступний тиждень.'
            )
        if skipped:
            messages.warning(
                request,
                f'Пропущено {skipped} днів — меню на ці дати вже існують. '
                f'Видаліть їх вручну якщо хочете перезаписати.'
            )
