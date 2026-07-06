from __future__ import annotations

LAYOUT_WARNING = (
    'Увага: занадто довгий текст або зображення неправильного розміру можуть зламати верстку сайту.'
)

IMAGE_WARNING = f'{LAYOUT_WARNING} Дотримуйтесь рекомендованих розмірів нижче.'

GUIDES: dict[str, str] = {
    'Doctor.slug': 'Латиниця, дефіси. Унікальний ідентифікатор для URL. Макс. 50 символів.',
    'Doctor.name': f'Макс. 120 символів. {LAYOUT_WARNING}',
    'Doctor.specialization': f'Макс. 160 символів. Коротко, 1–2 рядки в картці лікаря. {LAYOUT_WARNING}',
    'Doctor.bio': f'Коротка біографія для картки. Рекомендовано до 500 символів. {LAYOUT_WARNING}',
    'Doctor.experience_years': 'Число років досвіду (0–99).',
    'Doctor.initials': 'Макс. 8 символів. Якщо порожньо — генеруються з імені.',
    'Doctor.photo': (
        f'Квадратне фото: рекомендовано 400×400 px (мін. 224×224). '
        f'JPG/PNG/WebP, до 5 МБ. На сайті відображається колом 112×112 px. '
        f'Автоматично конвертується в WebP. {IMAGE_WARNING}'
    ),
    'Doctor.rating': 'Рейтинг від 0.0 до 5.0 (наприклад, 4.9).',
    'Doctor.patients_label': f'Макс. 32 символи (напр. «2400+ пацієнтів»). {LAYOUT_WARNING}',
    'Doctor.order': 'Порядок сортування в списку (менше — вище).',
    'Doctor.is_active': 'Зняти прапорець, щоб приховати лікаря на сайті.',
    'Advantage.icon': 'Іконка в картці переваги на головній (28×28 px).',
    'Advantage.title': f'Макс. 80 символів — заголовок картки. {LAYOUT_WARNING}',
    'Advantage.description': f'Макс. 160 символів — опис під заголовком. {LAYOUT_WARNING}',
    'Advantage.order': 'Порядок у сітці переваг.',
    'Advantage.is_alt': 'Помаранчева іконка замість зеленої.',
    'Advantage.is_active': 'Приховати перевагу на сайті.',
    'Service.slug': 'Латиниця для URL. Макс. 50 символів.',
    'Service.name': f'Макс. 120 символів — назва в картці послуги. {LAYOUT_WARNING}',
    'Service.short_description': f'Макс. 120 символів — підпис під назвою. {LAYOUT_WARNING}',
    'Service.full_description': f'Повний опис на сторінці послуги. Рекомендовано до 3000 символів. {LAYOUT_WARNING}',
    'Service.price_hint': f'Макс. 64 символи (напр. «від 350 грн»). {LAYOUT_WARNING}',
    'Service.icon': 'Іконка послуги в картці.',
    'Service.bullets': 'Список пунктів (JSON-масив рядків). Кожен пункт — до 120 символів.',
    'Service.is_urgent': 'Позначка «Терміново» на картці.',
    'Service.order': 'Порядок у списку послуг.',
    'Service.is_active': 'Приховати послугу на сайті.',
    'SiteSettings.clinic_name_line1': f'Макс. 64 символи — верхній рядок логотипу. {LAYOUT_WARNING}',
    'SiteSettings.clinic_name_line2': f'Макс. 64 символи — назва клініки. {LAYOUT_WARNING}',
    'SiteSettings.logo': (
        f'Квадратний логотип: рекомендовано 128×128 px. На сайті 40×40 px. '
        f'Автоматично конвертується в WebP. {IMAGE_WARNING}'
    ),
    'SiteSettings.tagline': f'Макс. 200 символів. {LAYOUT_WARNING}',
    'SiteSettings.address': f'Макс. 255 символів. {LAYOUT_WARNING}',
    'SiteSettings.phone_primary': 'Основний телефон для шапки та футера.',
    'SiteSettings.phone_secondary': 'Додатковий телефон (необовʼязково).',
    'SiteSettings.email': 'Електронна пошта клініки.',
    'SiteSettings.trust_label': f'Макс. 64 символи — смуга довіри. {LAYOUT_WARNING}',
    'SiteSettings.hours_label': f'Макс. 64 символи — години роботи. {LAYOUT_WARNING}',
    'SiteSettings.is_open_now': 'Показувати «Працюємо зараз» у смузі довіри.',
}

BLOCK_FIELD_HELP: dict[tuple[str, str], str] = {
    ('home', 'hero_title'): f'Макс. ~80 символів — головний заголовок. {LAYOUT_WARNING}',
    ('home', 'hero_lead'): f'Макс. ~600 символів — підзаголовок банера. {LAYOUT_WARNING}',
    ('home', 'hero_cta_booking'): f'Макс. ~24 символи — текст кнопки. {LAYOUT_WARNING}',
    ('home', 'hero_cta_suffix'): f'Макс. ~16 символів — суфікс кнопки. {LAYOUT_WARNING}',
    ('home', 'hero_cta_phone'): f'Макс. ~20 символів — текст кнопки телефону. {LAYOUT_WARNING}',
    ('home', 'hero_image'): (
        f'Портретне фото: рекомендовано 800×1000 px. На сайті масштабується до ~720 px висоти. '
        f'Автоматично конвертується в WebP. {IMAGE_WARNING}'
    ),
    ('home', 'hero_image_alt'): f'Макс. ~120 символів — alt-текст для доступності. {LAYOUT_WARNING}',
    ('home', 'hero_stat_number'): f'Макс. ~12 символів (напр. «24/7»). {LAYOUT_WARNING}',
    ('home', 'hero_stat_label'): f'Макс. ~48 символів — підпис під числом. {LAYOUT_WARNING}',
    ('home', 'advantages_section_title'): f'Макс. ~64 символи — заголовок секції. {LAYOUT_WARNING}',
    ('home', 'services_preview_tag'): f'Макс. ~24 символи — мітка секції. {LAYOUT_WARNING}',
    ('home', 'services_preview_title'): f'Макс. ~64 символи. {LAYOUT_WARNING}',
    ('home', 'services_preview_hint'): f'Макс. ~120 символів — підказка під заголовком. {LAYOUT_WARNING}',
    ('home', 'services_preview_more_label'): f'Макс. ~32 символи — текст посилання. {LAYOUT_WARNING}',
    ('home', 'doctors_preview_tag'): f'Макс. ~24 символи. {LAYOUT_WARNING}',
    ('home', 'doctors_preview_title'): f'Макс. ~64 символи. {LAYOUT_WARNING}',
    ('home', 'doctors_preview_note'): f'Макс. ~200 символів — примітка під заголовком. {LAYOUT_WARNING}',
    ('services', 'header_tag'): f'Макс. ~24 символи — мітка сторінки. {LAYOUT_WARNING}',
    ('services', 'header_title'): f'Макс. ~80 символів — H1 сторінки. {LAYOUT_WARNING}',
    ('services', 'header_lead'): f'Макс. ~200 символів — підзаголовок. {LAYOUT_WARNING}',
    ('doctors', 'header_tag'): f'Макс. ~24 символи. {LAYOUT_WARNING}',
    ('doctors', 'header_title'): f'Макс. ~80 символів. {LAYOUT_WARNING}',
    ('doctors', 'header_lead'): f'Макс. ~200 символів. {LAYOUT_WARNING}',
    ('contacts', 'header_tag'): f'Макс. ~24 символи. {LAYOUT_WARNING}',
    ('contacts', 'header_title'): f'Макс. ~80 символів. {LAYOUT_WARNING}',
    ('contacts', 'header_lead'): f'Макс. ~200 символів. {LAYOUT_WARNING}',
    ('contacts', 'clinic_block_title'): f'Макс. ~48 символів. {LAYOUT_WARNING}',
    ('contacts', 'form_block_title'): f'Макс. ~48 символів. {LAYOUT_WARNING}',
    ('site', 'footer_instagram_url'): 'Повне посилання на Instagram (https://...).',
    ('site', 'footer_telegram_url'): 'Повне посилання на Telegram (https://...).',
}


def guide_key(model_label: str, field_name: str) -> str:
    return f'{model_label}.{field_name}'


def get_guide(model_label: str, field_name: str) -> str:
    return GUIDES.get(guide_key(model_label, field_name), '')


def get_block_help(page: str, key: str) -> str:
    return BLOCK_FIELD_HELP.get((page, key), '')
