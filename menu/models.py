from django.db import models
from django.urls import reverse


class DailyMenu(models.Model):
    """Меню на конкретний день для всіх груп закладу.
       Поля «II сніданок» та «Вечеря» необовʼязкові — вечеря лише для чергових
       груп з режимом 12 годин."""
    date = models.DateField('Дата', unique=True)

    breakfast        = models.TextField('🥣 Сніданок',         blank=True)
    second_breakfast = models.TextField('🍎 II сніданок',       blank=True,
                                          help_text='Часто це фрукт або сік. Необовʼязково.')
    lunch            = models.TextField('🍲 Обід',             blank=True)
    snack            = models.TextField('🥨 Полуденок',        blank=True)
    dinner           = models.TextField('🥛 Вечеря',           blank=True,
                                          help_text='Для чергових груп (12 годин). Необовʼязково.')

    note = models.CharField(
        'Примітка дня', max_length=300, blank=True,
        help_text='Наприклад: «Святкове меню до Дня матері» або позначення алергенів.'
    )
    is_published = models.BooleanField('Опубліковано', default=True)
    created_at = models.DateTimeField('Створено', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    class Meta:
        verbose_name = 'Меню на день'
        verbose_name_plural = 'Денні меню'
        ordering = ['-date']
        indexes = [models.Index(fields=['date'])]

    def __str__(self):
        return f"Меню на {self.date.strftime('%d.%m.%Y')}"

    def get_absolute_url(self):
        return f"{reverse('menu:index')}?date={self.date.isoformat()}"

    @property
    def has_any_meal(self):
        return any([
            self.breakfast, self.second_breakfast,
            self.lunch, self.snack, self.dinner,
        ])
