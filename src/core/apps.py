from django.apps import AppConfig
from django.conf import settings
from django.core.signals import request_started
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.template import engines


def _connect_site_block_cache_signals() -> None:
    from core.context_processors import invalidate_site_blocks_cache
    from core.models import SiteBlock

    @receiver(post_save, sender=SiteBlock, dispatch_uid='core_siteblock_save_cache')
    def _clear_cache_on_save(sender, instance, **kwargs) -> None:
        invalidate_site_blocks_cache()

    @receiver(post_delete, sender=SiteBlock, dispatch_uid='core_siteblock_delete_cache')
    def _clear_cache_on_delete(sender, instance, **kwargs) -> None:
        invalidate_site_blocks_cache()


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Налаштування сайту'

    def ready(self) -> None:
        _connect_site_block_cache_signals()

        if not settings.DEBUG:
            return

        @receiver(request_started, dispatch_uid='develop_clear_template_cache')
        def _clear_template_cache_on_request(**kwargs) -> None:
            """rundev disables autoreload; reload templates from disk each request."""
            for backend in engines.all():
                inner = getattr(backend, 'engine', None)
                if inner is not None and hasattr(inner, 'templates'):
                    inner.templates.clear()
