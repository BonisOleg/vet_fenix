from django.contrib import admin
from unfold.admin import ModelAdmin

from core.admin_site_content import site_content_section_view
from core.admin_utils import ReadableUnfoldFieldsMixin, SingletonModelAdminMixin
from core.models import (
    ContactsClinicInfoSettings,
    ContactsFormSettings,
    ContactsMapSettings,
    ContactsPageHeaderSettings,
    DoctorsPageHeaderSettings,
    FooterSocialSettings,
    HomeAdvantagesSettings,
    HomeDoctorsPreviewSettings,
    HomeHeroSettings,
    HomeServicesPreviewSettings,
    ServicesPageHeaderSettings,
    SiteSettings,
    TrustStripSettings,
)


class SiteContentSectionAdmin(SingletonModelAdminMixin, ReadableUnfoldFieldsMixin, ModelAdmin):
    page_slug: str = ''
    section_slug: str = ''

    def change_view(self, request, object_id, form_url='', extra_context=None):
        return site_content_section_view(
            request,
            self.page_slug,
            self.section_slug,
            model_admin=self,
        )


_SECTION_MODELS: tuple[tuple[type[SiteSettings], str, str], ...] = (
    (HomeHeroSettings, 'home', 'hero'),
    (HomeAdvantagesSettings, 'home', 'advantages'),
    (HomeServicesPreviewSettings, 'home', 'services-preview'),
    (HomeDoctorsPreviewSettings, 'home', 'doctors-preview'),
    (ServicesPageHeaderSettings, 'services', 'header'),
    (DoctorsPageHeaderSettings, 'doctors', 'header'),
    (ContactsPageHeaderSettings, 'contacts', 'header'),
    (ContactsClinicInfoSettings, 'contacts', 'clinic-info'),
    (ContactsFormSettings, 'contacts', 'contact-form'),
    (ContactsMapSettings, 'contacts', 'map'),
    (TrustStripSettings, 'site', 'trust-strip'),
    (FooterSocialSettings, 'site', 'footer-social'),
)


def register_site_content_section_admins() -> None:
    for model, page_slug, section_slug in _SECTION_MODELS:
        class SectionAdmin(SiteContentSectionAdmin):
            pass

        SectionAdmin.__name__ = f'{model.__name__}Admin'
        SectionAdmin.page_slug = page_slug
        SectionAdmin.section_slug = section_slug
        admin.site.register(model, SectionAdmin)


register_site_content_section_admins()
