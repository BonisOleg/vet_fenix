from django.contrib import admin
from unfold.admin import ModelAdmin

from core.admin_mixins import ReadableUnfoldFieldsMixin
from bookings.models import AppointmentRequest, CallbackLead


@admin.register(CallbackLead)
class CallbackLeadAdmin(ReadableUnfoldFieldsMixin, ModelAdmin):
    list_display = ('name', 'phone', 'service', 'source_page', 'created_at')
    list_filter = ('service', 'source_page', 'created_at')
    search_fields = ('name', 'phone', 'comment')
    readonly_fields = ('created_at', 'source_page')
    date_hierarchy = 'created_at'

    def has_add_permission(self, request) -> bool:
        return False


@admin.register(AppointmentRequest)
class AppointmentRequestAdmin(ReadableUnfoldFieldsMixin, ModelAdmin):
    list_display = (
        'owner_name',
        'phone',
        'service',
        'doctor',
        'pet_name',
        'pet_type',
        'preferred_date',
        'preferred_time',
        'created_at',
        'status',
    )
    list_filter = ('status', 'preferred_date', 'service', 'pet_type')
    search_fields = ('owner_name', 'phone', 'pet_name', 'comment')
    readonly_fields = ('created_at', 'source_page')
    date_hierarchy = 'created_at'
    list_editable = ('status',)

    fieldsets = (
        (
            'Клієнт',
            {
                'fields': (
                    'owner_name',
                    'phone',
                    'pet_name',
                    'pet_type',
                ),
            },
        ),
        (
            'Запис',
            {
                'fields': (
                    'service',
                    'doctor',
                    'preferred_date',
                    'preferred_time',
                    'status',
                    'comment',
                ),
            },
        ),
        (
            'Мета',
            {
                'fields': (
                    'source_page',
                    'created_at',
                ),
            },
        ),
    )

    def has_add_permission(self, request) -> bool:
        return False
