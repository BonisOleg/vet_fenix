from __future__ import annotations

from django.http import HttpResponseRedirect
from django.urls import reverse

from core.admin_site_content_widgets import apply_readable_widget
from core.models import SiteSettings


class ReadableUnfoldFieldsMixin:
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if formfield is not None:
            formfield.widget = apply_readable_widget(formfield.widget)
        return formfield


class AdminFieldGuidesMixin:
    guide_model_label: str = ''

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if formfield is None:
            return formfield
        from core.admin_field_guides import get_guide

        model_label = self.guide_model_label or self.model._meta.label.split('.')[-1]
        guide = get_guide(model_label, db_field.name)
        if guide:
            formfield.help_text = guide
        return formfield


class SingletonModelAdminMixin:
    def has_add_permission(self, request) -> bool:
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = SiteSettings.objects.get_or_create(pk=1)
        url_name = f'admin:core_{self.model._meta.model_name}_change'
        return HttpResponseRedirect(reverse(url_name, args=[obj.pk]))
