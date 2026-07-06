from django.contrib import admin
from unfold.admin import ModelAdmin

from core.admin_utils import ReadableUnfoldFieldsMixin, SingletonModelAdminMixin
from core.models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(ReadableUnfoldFieldsMixin, SingletonModelAdminMixin, ModelAdmin):
    list_display = ('clinic_name_line1', 'clinic_name_line2', 'phone_primary')

    fieldsets = (
        (
            'Бренд',
            {
                'classes': ('collapse',),
                'fields': (
                    'clinic_name_line1',
                    'clinic_name_line2',
                    'logo',
                    'tagline',
                    'trust_label',
                    'hours_label',
                    'is_open_now',
                ),
            },
        ),
        (
            'Контакти',
            {
                'classes': ('collapse',),
                'fields': (
                    'address',
                    'phone_primary',
                    'phone_secondary',
                    'email',
                ),
            },
        ),
    )


from core import admin_site_content_proxies  # noqa: E402, F401
