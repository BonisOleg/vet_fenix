from django.db.models.signals import pre_save
from django.dispatch import receiver

from clinic.models import Doctor
from core.models import SiteBlock, SiteSettings
from core.utils.image_upload import (
    CMS_DEFAULT,
    CMS_IMAGE_PROFILES,
    DOCTOR_PHOTO,
    SITE_LOGO,
    process_image_field,
)


@receiver(pre_save, sender=Doctor)
def convert_doctor_photo_to_webp(sender, instance: Doctor, **kwargs) -> None:
    process_image_field(instance, 'photo', DOCTOR_PHOTO)


@receiver(pre_save, sender=SiteSettings)
def convert_site_logo_to_webp(sender, instance: SiteSettings, **kwargs) -> None:
    process_image_field(instance, 'logo', SITE_LOGO)


@receiver(pre_save, sender=SiteBlock)
def convert_site_block_image_to_webp(sender, instance: SiteBlock, **kwargs) -> None:
    if instance.content_type != SiteBlock.ContentType.IMAGE:
        return
    profile = CMS_IMAGE_PROFILES.get((instance.page, instance.key), CMS_DEFAULT)
    process_image_field(instance, 'image', profile)
