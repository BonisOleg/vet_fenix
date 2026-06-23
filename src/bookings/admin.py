from django.contrib import admin

from bookings.models import AppointmentRequest, CallbackLead


@admin.register(CallbackLead)
class CallbackLeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'service', 'source_page', 'created_at')
    list_filter = ('service', 'created_at')
    search_fields = ('name', 'phone', 'comment')
    readonly_fields = ('created_at', 'source_page')


@admin.register(AppointmentRequest)
class AppointmentRequestAdmin(admin.ModelAdmin):
    list_display = (
        'owner_name',
        'phone',
        'service',
        'doctor',
        'preferred_date',
        'preferred_time',
        'status',
        'created_at',
    )
    list_filter = ('status', 'preferred_date', 'service')
    search_fields = ('owner_name', 'phone', 'pet_name')
    readonly_fields = ('created_at', 'source_page')
