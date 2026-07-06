from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, TestCase, override_settings
from PIL import Image

from clinic.models import Doctor
from core.utils.image_upload import (
    optimize_image_to_webp,
    should_process_image,
    webp_filename,
)


class ImageUploadUtilsTests(SimpleTestCase):
    def test_webp_filename_preserves_directory(self):
        self.assertEqual(webp_filename('doctors/photo.jpg'), 'doctors/photo.webp')

    def test_should_process_image_for_new_upload(self):
        upload = SimpleUploadedFile('test.jpg', b'fake', content_type='image/jpeg')
        doctor = Doctor()
        field = Doctor._meta.get_field('photo')
        field_file = field.attr_class(doctor, field, 'doctors/test.jpg')
        field_file.file = upload
        field_file._committed = False
        self.assertTrue(should_process_image(field_file))

    def test_should_process_precommitted_png_on_new_instance(self):
        doctor = Doctor()
        field = Doctor._meta.get_field('photo')
        field_file = field.attr_class(doctor, field, 'doctors/test.png')
        field_file._committed = True
        self.assertTrue(should_process_image(field_file, old_name=None))

    def test_optimize_image_to_webp_returns_webp_bytes(self):
        image = Image.new('RGB', (1200, 900), color=(255, 120, 40))
        buffer = BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)
        upload = SimpleUploadedFile('hero.jpg', buffer.read(), content_type='image/jpeg')

        content = optimize_image_to_webp(upload, max_size=(800, 800))
        self.assertTrue(content.read(4) != b'')


@override_settings(MEDIA_ROOT='/tmp/vet-test-media-webp')
class DoctorWebpSignalTests(TestCase):
    def test_doctor_photo_converted_to_webp_on_save(self):
        import os

        from django.conf import settings

        from clinic.models import Doctor

        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

        image = Image.new('RGB', (600, 600), color=(200, 100, 50))
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)

        doctor = Doctor(
            slug='test-doc',
            name='Тест Лікар',
            specialization='Терапевт',
            experience_years=5,
        )
        doctor.photo.save('test.png', SimpleUploadedFile('test.png', buffer.read()), save=False)
        doctor.save()

        self.assertTrue(doctor.photo.name.endswith('.webp'))
