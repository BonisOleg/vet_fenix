from django.contrib import admin

from clinic.models import Advantage, ContactMessage, Doctor, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_urgent', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'specialization',
        'experience_years',
        'rating',
        'patients_label',
        'order',
        'is_active',
    )
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    fields = (
        'slug',
        'name',
        'specialization',
        'bio',
        'experience_years',
        'initials',
        'photo',
        'rating',
        'patients_label',
        'order',
        'is_active',
    )


@admin.register(Advantage)
class AdvantageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_alt')
    list_editable = ('order', 'is_alt')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at')
    search_fields = ('name', 'phone', 'message')
    readonly_fields = ('created_at',)
