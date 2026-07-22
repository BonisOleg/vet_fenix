from django.contrib import admin
from django.utils.html import format_html
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin
from unfold.widgets import UnfoldAdminImageFieldWidget

from core.admin_mixins import AdminFieldGuidesMixin, ReadableUnfoldFieldsMixin
from clinic.models import Advantage, ContactMessage, Doctor, Service


@admin.register(Service)
class ServiceAdmin(AdminFieldGuidesMixin, ReadableUnfoldFieldsMixin, ModelAdmin):
    guide_model_label = 'Service'
    list_display = ('name', 'slug', 'price_hint', 'is_urgent', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_urgent', 'is_active', 'icon')
    search_fields = ('name', 'slug', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'name',
                    'slug',
                    'icon',
                    'short_description',
                    'full_description',
                    'price_hint',
                    'bullets',
                    'is_urgent',
                    'order',
                    'is_active',
                ),
            },
        ),
    )


@admin.register(Doctor)
class DoctorAdmin(AdminFieldGuidesMixin, ReadableUnfoldFieldsMixin, ModelAdmin):
    guide_model_label = 'Doctor'
    list_display = (
        'get_photo_preview',
        'name',
        'specialization',
        'experience_years',
        'patients_label',
        'order',
        'is_active',
    )
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'specialization', 'bio')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('get_photo_preview',)
    ordering = ('order', 'name')

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'slug',
                    'name',
                    'specialization',
                    'bio',
                    'experience_years',
                    'initials',
                    'patients_label',
                    'order',
                    'is_active',
                ),
            },
        ),
        (
            'Фото',
            {
                'fields': (
                    'photo',
                    'get_photo_preview',
                ),
            },
        ),
    )

    @admin.display(description='Фото')
    def get_photo_preview(self, obj: Doctor) -> str:
        if obj.photo:
            return format_html(
                '<img src="{}" alt="{}" style="max-height:120px;border-radius:8px;" />',
                obj.photo.url,
                obj.name,
            )
        return '—'

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'bio':
            kwargs['widget'] = TinyMCE()
        if db_field.name == 'photo':
            kwargs['widget'] = UnfoldAdminImageFieldWidget()
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(Advantage)
class AdvantageAdmin(AdminFieldGuidesMixin, ReadableUnfoldFieldsMixin, ModelAdmin):
    guide_model_label = 'Advantage'
    list_display = ('title', 'icon', 'order', 'is_alt', 'is_active')
    list_editable = ('order', 'is_alt', 'is_active')
    list_filter = ('icon', 'is_alt')
    search_fields = ('title', 'description')
    ordering = ('order',)


@admin.register(ContactMessage)
class ContactMessageAdmin(ReadableUnfoldFieldsMixin, ModelAdmin):
    list_display = ('name', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'phone', 'message')
    readonly_fields = ('name', 'phone', 'message', 'created_at')
    date_hierarchy = 'created_at'

    def has_add_permission(self, request) -> bool:
        return False
