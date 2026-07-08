from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.widgets import UnfoldAdminImageFieldWidget

from core.admin_utils import AdminFieldGuidesMixin, ReadableUnfoldFieldsMixin, SingletonModelAdminMixin
from core.models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(AdminFieldGuidesMixin, ReadableUnfoldFieldsMixin, SingletonModelAdminMixin, ModelAdmin):
    guide_model_label = 'SiteSettings'
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
                    'reassessment_hours_label',
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

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'logo':
            kwargs['widget'] = UnfoldAdminImageFieldWidget()
        return super().formfield_for_dbfield(db_field, request, **kwargs)


from core import admin_site_content_proxies  # noqa: E402, F401
