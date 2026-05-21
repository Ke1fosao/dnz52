from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        """Налаштування Django-адмінки під ЗДО №52 — виконується одразу при старті."""
        from django.contrib import admin
        from .admin_helpers import customize_app_list

        # Брендинг адмінки (з'являється у хедері та в title вкладки)
        admin.site.site_header = 'ЗДО №52 — Адміністрування'
        admin.site.site_title  = 'Адмінка ЗДО №52'
        admin.site.index_title = 'Вітаємо у панелі управління сайтом'

        # Кастомна стартова сторінка з підказками і швидкими діями
        admin.site.index_template = 'admin/dnz_index.html'

        # Перегрупуємо й перейменуємо розділи у бічному списку
        customize_app_list(admin.site)
