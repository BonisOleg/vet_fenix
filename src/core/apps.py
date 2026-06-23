from django.apps import AppConfig
from django.conf import settings
from django.core.signals import request_started
from django.dispatch import receiver
from django.template import engines


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Налаштування сайту'

    def ready(self) -> None:
        if not settings.DEBUG:
            return

        @receiver(request_started, dispatch_uid='develop_clear_template_cache')
        def _clear_template_cache_on_request(**kwargs) -> None:
            """rundev disables autoreload; reload templates from disk each request."""
            for backend in engines.all():
                inner = getattr(backend, 'engine', None)
                if inner is not None and hasattr(inner, 'templates'):
                    inner.templates.clear()
