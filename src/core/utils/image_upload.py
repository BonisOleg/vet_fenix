from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import PurePosixPath

from django.core.files.base import ContentFile
from PIL import Image


@dataclass(frozen=True)
class ImageProfile:
    max_size: tuple[int, int]
    quality: int = 85


DOCTOR_PHOTO = ImageProfile(max_size=(800, 800))
SITE_LOGO = ImageProfile(max_size=(256, 256))
CMS_HERO = ImageProfile(max_size=(1600, 2000))
CMS_DEFAULT = ImageProfile(max_size=(1600, 1600))

CMS_IMAGE_PROFILES: dict[tuple[str, str], ImageProfile] = {
    ('home', 'hero_image'): CMS_HERO,
}


def optimize_image_to_webp(
    uploaded_file,
    *,
    max_size: tuple[int, int],
    quality: int = 85,
) -> ContentFile:
    uploaded_file.seek(0)
    image = Image.open(uploaded_file)
    image.load()

    if image.mode not in ('RGB', 'RGBA'):
        image = image.convert('RGBA')

    max_width, max_height = max_size
    image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

    if image.mode == 'RGBA':
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[3])
        image = background
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    buffer = BytesIO()
    image.save(buffer, format='WEBP', quality=quality, method=6)
    buffer.seek(0)
    return ContentFile(buffer.read())


def webp_filename(original_name: str) -> str:
    path = PurePosixPath(original_name)
    if path.parent.parts:
        return str(path.parent / f'{path.stem}.webp')
    return f'{path.stem}.webp'


def should_process_image(field_file, *, old_name: str | None = None) -> bool:
    if not field_file or not field_file.name:
        return False

    current = field_file.name
    if old_name == current and current.lower().endswith('.webp'):
        return False

    if not getattr(field_file, '_committed', True):
        return True

    if old_name is not None and old_name != current:
        return True

    return old_name is None and not current.lower().endswith('.webp')


def get_stored_field_name(instance, field_name: str) -> str | None:
    if not instance.pk:
        return None
    model = type(instance)
    try:
        stored = model.objects.only(field_name).get(pk=instance.pk)
    except model.DoesNotExist:
        return None
    field = getattr(stored, field_name)
    return field.name if field else None


def process_image_field(instance, field_name: str, profile: ImageProfile) -> None:
    field_file = getattr(instance, field_name)
    old_name = get_stored_field_name(instance, field_name)
    if not should_process_image(field_file, old_name=old_name):
        return
    content = optimize_image_to_webp(
        field_file,
        max_size=profile.max_size,
        quality=profile.quality,
    )
    new_name = webp_filename(field_file.name)
    field_file.save(new_name, content, save=False)

    if old_name and old_name != new_name:
        field_file.storage.delete(old_name)
