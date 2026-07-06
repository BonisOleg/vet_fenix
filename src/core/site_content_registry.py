from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

from django.urls import reverse_lazy

from core.block_defaults import BLOCK_FIELD_LABELS


@dataclass(frozen=True)
class FieldGroup:
    title: str
    block_keys: tuple[str, ...]


@dataclass(frozen=True)
class ContentSection:
    slug: str
    page_slug: str
    title: str
    blocks: tuple[tuple[str, str], ...]
    sidebar_title: str = ''
    sidebar_icon: str = 'edit_note'
    preview_url: str = '/'
    description: str = ''
    visibility_key: str = ''
    field_groups: tuple[FieldGroup, ...] = field(default_factory=tuple)
    admin_model_name: str = ''


CONTENT_SECTIONS: tuple[ContentSection, ...] = (
    ContentSection(
        slug='hero',
        page_slug='home',
        title='Головний банер',
        sidebar_title='Головна — Банер',
        sidebar_icon='image',
        preview_url='/',
        admin_model_name='homeherosettings',
        description='Заголовок, текст, кнопки та фото головного банера.',
        visibility_key='hero_section_visible',
        blocks=(
            ('home', 'hero_title'),
            ('home', 'hero_lead'),
            ('home', 'hero_cta_booking'),
            ('home', 'hero_cta_suffix'),
            ('home', 'hero_cta_phone'),
            ('home', 'hero_image'),
            ('home', 'hero_image_alt'),
            ('home', 'hero_stat_number'),
            ('home', 'hero_stat_label'),
        ),
        field_groups=(
            FieldGroup('Заголовок і текст', ('hero_title', 'hero_lead')),
            FieldGroup('Кнопки', ('hero_cta_booking', 'hero_cta_suffix', 'hero_cta_phone')),
            FieldGroup('Зображення', ('hero_image', 'hero_image_alt')),
            FieldGroup('Статистика', ('hero_stat_number', 'hero_stat_label')),
        ),
    ),
    ContentSection(
        slug='advantages',
        page_slug='home',
        title='Переваги',
        sidebar_title='Головна — Переваги',
        sidebar_icon='star',
        preview_url='/#perevahy',
        admin_model_name='homeadvantagessettings',
        visibility_key='advantages_section_visible',
        blocks=(('home', 'advantages_section_title'),),
        field_groups=(FieldGroup('Заголовок секції', ('advantages_section_title',)),),
    ),
    ContentSection(
        slug='services-preview',
        page_slug='home',
        title='Послуги на головній',
        sidebar_title='Головна — Послуги',
        sidebar_icon='medical_services',
        preview_url='/#poslugy',
        admin_model_name='homeservicespreviewsettings',
        visibility_key='services_preview_section_visible',
        blocks=(
            ('home', 'services_preview_tag'),
            ('home', 'services_preview_title'),
            ('home', 'services_preview_hint'),
            ('home', 'services_preview_more_label'),
        ),
        field_groups=(
            FieldGroup(
                'Заголовок і підказки',
                ('services_preview_tag', 'services_preview_title', 'services_preview_hint', 'services_preview_more_label'),
            ),
        ),
    ),
    ContentSection(
        slug='doctors-preview',
        page_slug='home',
        title='Лікарі на головній',
        sidebar_title='Головна — Лікарі',
        sidebar_icon='person',
        preview_url='/#likari',
        admin_model_name='homedoctorspreviewsettings',
        visibility_key='doctors_preview_section_visible',
        blocks=(
            ('home', 'doctors_preview_tag'),
            ('home', 'doctors_preview_title'),
            ('home', 'doctors_preview_note'),
        ),
        field_groups=(
            FieldGroup(
                'Заголовок і примітка',
                ('doctors_preview_tag', 'doctors_preview_title', 'doctors_preview_note'),
            ),
        ),
    ),
    ContentSection(
        slug='header',
        page_slug='services',
        title='Шапка сторінки послуг',
        sidebar_title='Послуги — Заголовок',
        sidebar_icon='title',
        preview_url='/poslugy/',
        admin_model_name='servicespageheadersettings',
        visibility_key='header_section_visible',
        blocks=(
            ('services', 'header_tag'),
            ('services', 'header_title'),
            ('services', 'header_lead'),
        ),
        field_groups=(FieldGroup('Заголовок сторінки', ('header_tag', 'header_title', 'header_lead')),),
    ),
    ContentSection(
        slug='header',
        page_slug='doctors',
        title='Шапка сторінки лікарів',
        sidebar_title='Лікарі — Заголовок',
        sidebar_icon='title',
        preview_url='/likari/',
        admin_model_name='doctorspageheadersettings',
        visibility_key='header_section_visible',
        blocks=(
            ('doctors', 'header_tag'),
            ('doctors', 'header_title'),
            ('doctors', 'header_lead'),
        ),
        field_groups=(FieldGroup('Заголовок сторінки', ('header_tag', 'header_title', 'header_lead')),),
    ),
    ContentSection(
        slug='header',
        page_slug='contacts',
        title='Шапка сторінки контактів',
        sidebar_title='Контакти — Заголовок',
        sidebar_icon='title',
        preview_url='/kontakty/',
        admin_model_name='contactspageheadersettings',
        visibility_key='header_section_visible',
        blocks=(
            ('contacts', 'header_tag'),
            ('contacts', 'header_title'),
            ('contacts', 'header_lead'),
        ),
        field_groups=(FieldGroup('Заголовок сторінки', ('header_tag', 'header_title', 'header_lead')),),
    ),
    ContentSection(
        slug='clinic-info',
        page_slug='contacts',
        title='Блок «Клініка»',
        sidebar_title='Контакти — Клініка',
        sidebar_icon='location_on',
        preview_url='/kontakty/',
        admin_model_name='contactsclinicinfosettings',
        visibility_key='clinic_section_visible',
        blocks=(('contacts', 'clinic_block_title'),),
        field_groups=(FieldGroup('Заголовок блоку', ('clinic_block_title',)),),
    ),
    ContentSection(
        slug='contact-form',
        page_slug='contacts',
        title='Блок форми',
        sidebar_title='Контакти — Форма',
        sidebar_icon='mail',
        preview_url='/kontakty/',
        admin_model_name='contactsformsettings',
        visibility_key='form_section_visible',
        blocks=(('contacts', 'form_block_title'),),
        field_groups=(FieldGroup('Заголовок блоку', ('form_block_title',)),),
    ),
    ContentSection(
        slug='map',
        page_slug='contacts',
        title='Карта',
        sidebar_title='Контакти — Карта',
        sidebar_icon='map',
        preview_url='/kontakty/',
        admin_model_name='contactsmapsettings',
        visibility_key='map_section_visible',
        blocks=(),
        description='Увімкнення або вимкнення Google Maps на сторінці контактів.',
    ),
    ContentSection(
        slug='trust-strip',
        page_slug='site',
        title='Смуга довіри',
        sidebar_title='Смуга довіри',
        sidebar_icon='verified',
        preview_url='/',
        admin_model_name='truststripsettings',
        visibility_key='trust_strip_section_visible',
        blocks=(),
        description='Смуга «Працюємо зараз» під шапкою. Текст береться з налаштувань сайту.',
    ),
    ContentSection(
        slug='footer-social',
        page_slug='site',
        title='Соцмережі у футері',
        sidebar_title='Футер — Соцмережі',
        sidebar_icon='share',
        preview_url='/',
        admin_model_name='footersocialsettings',
        visibility_key='footer_social_section_visible',
        blocks=(
            ('site', 'footer_instagram_url'),
            ('site', 'footer_telegram_url'),
        ),
        field_groups=(FieldGroup('Посилання', ('footer_instagram_url', 'footer_telegram_url')),),
    ),
)

SECTION_BY_ADMIN_MODEL = {section.admin_model_name: section for section in CONTENT_SECTIONS}


def get_block_field_label(page: str, key: str) -> str:
    return BLOCK_FIELD_LABELS.get((page, key), key.replace('_', ' ').capitalize())


def get_section(page_slug: str, section_slug: str) -> ContentSection:
    for section in CONTENT_SECTIONS:
        if section.page_slug == page_slug and section.slug == section_slug:
            return section
    raise KeyError(f'Section {section_slug!r} not found on page {page_slug!r}')


def get_section_by_admin_model(admin_model_name: str) -> ContentSection:
    try:
        return SECTION_BY_ADMIN_MODEL[admin_model_name]
    except KeyError as exc:
        raise KeyError(f'Section for admin model {admin_model_name!r} not found') from exc


def iter_section_blocks(section: ContentSection) -> Iterator[tuple[str, str]]:
    yield from section.blocks
    if not section.visibility_key:
        return
    if section.blocks:
        page = section.blocks[0][0]
    elif section.page_slug == 'contacts':
        page = 'contacts'
    else:
        page = section.page_slug
    yield page, section.visibility_key


def all_registry_block_keys() -> set[tuple[str, str]]:
    keys: set[tuple[str, str]] = set()
    for section in CONTENT_SECTIONS:
        keys.update(iter_section_blocks(section))
    return keys


def build_content_sidebar_items() -> list[dict]:
    return [
        {
            'title': section.sidebar_title or section.title,
            'icon': section.sidebar_icon,
            'link': reverse_lazy(f'admin:core_{section.admin_model_name}_changelist'),
        }
        for section in CONTENT_SECTIONS
    ]


def get_visibility_block_key(page_slug: str, section_slug: str) -> str:
    section = get_section(page_slug, section_slug)
    return section.visibility_key
