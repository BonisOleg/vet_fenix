HERO_LEAD_DEFAULT = (
    'Ветеринарна клініка «Фенікс» надає широкий спектр послуг для Ваших домашніх улюбленців. '
    'Наші фахівці працюють за актуальними протоколами, спираючись на доказову медицину. '
    'Клініка забезпечена новітнім обладнанням, що допомагає у швидкій діагностиці пацієнтів. '
    'З основних переваг — цілодобовий стаціонар інтенсивної терапії та реанімації. '
    'Постійне навчання, поглиблення знань та навичок персоналу, використання сучасних методів '
    'діагностики — шлях до успіху у лікуванні Ваших хвостиків.'
)

BLOCK_FIELD_LABELS: dict[tuple[str, str], str] = {
    ('home', 'hero_title'): 'Заголовок',
    ('home', 'hero_lead'): 'Підзаголовок',
    ('home', 'hero_cta_booking'): 'Текст кнопки «Записатись»',
    ('home', 'hero_cta_suffix'): 'Суфікс кнопки (напр. « онлайн»)',
    ('home', 'hero_cta_phone'): 'Текст кнопки «Подзвонити»',
    ('home', 'hero_image'): 'Фото банера',
    ('home', 'hero_image_alt'): 'Alt-текст фото',
    ('home', 'hero_stat_number'): 'Банер картка (число)',
    ('home', 'hero_stat_label'): 'Банер картка (підпис)',
    ('home', 'advantages_section_title'): 'Заголовок секції',
    ('home', 'services_preview_tag'): 'Мітка',
    ('home', 'services_preview_title'): 'Заголовок',
    ('home', 'services_preview_hint'): 'Підказка',
    ('home', 'services_preview_more_label'): 'Посилання «Детальніше»',
    ('home', 'doctors_preview_tag'): 'Мітка',
    ('home', 'doctors_preview_title'): 'Заголовок',
    ('home', 'doctors_preview_note'): 'Примітка',
    ('services', 'header_tag'): 'Мітка',
    ('services', 'header_title'): 'Заголовок',
    ('services', 'header_lead'): 'Підзаголовок',
    ('doctors', 'header_tag'): 'Мітка',
    ('doctors', 'header_title'): 'Заголовок',
    ('doctors', 'header_lead'): 'Підзаголовок',
    ('contacts', 'header_tag'): 'Мітка',
    ('contacts', 'header_title'): 'Заголовок',
    ('contacts', 'header_lead'): 'Підзаголовок',
    ('contacts', 'clinic_block_title'): 'Заголовок блоку',
    ('contacts', 'form_block_title'): 'Заголовок блоку',
    ('site', 'footer_instagram_url'): 'Посилання Instagram',
    ('site', 'footer_telegram_url'): 'Посилання Telegram',
}

BLOCK_DEFAULTS: dict[tuple[str, str], str] = {
    ('home', 'hero_title'): 'Турбота про ваших улюбленців — цілодобово',
    ('home', 'hero_lead'): HERO_LEAD_DEFAULT,
    ('home', 'hero_cta_booking'): 'Записатись',
    ('home', 'hero_cta_suffix'): ' онлайн',
    ('home', 'hero_cta_phone'): 'Подзвонити',
    ('home', 'hero_image_alt'): 'Шотландський кіт — улюбленець клініки',
    ('home', 'hero_stat_number'): '24/7',
    ('home', 'hero_stat_label'): 'стаціонар інтенсивної терапії',
    ('home', 'hero_section_visible'): '1',
    ('home', 'advantages_section_title'): 'Чому обирають Фенікс',
    ('home', 'advantages_section_visible'): '1',
    ('home', 'services_preview_tag'): 'Послуги',
    ('home', 'services_preview_title'): 'Наші послуги',
    ('home', 'services_preview_hint'): 'Натисніть послугу, щоб переглянути деталі.',
    ('home', 'services_preview_more_label'): 'Детальніше →',
    ('home', 'services_preview_section_visible'): '1',
    ('home', 'doctors_preview_tag'): 'Команда',
    ('home', 'doctors_preview_title'): 'Лікарі, яким довіряють',
    ('home', 'doctors_preview_note'): (
        'Наші лікарі працюють за актуальними міжнародними протоколами, '
        'а сучасне діагностичне обладнання дозволяє виявляти захворювання на ранніх стадіях.'
    ),
    ('home', 'doctors_preview_section_visible'): '1',
    ('services', 'header_tag'): 'Послуги',
    ('services', 'header_title'): 'Все, що потрібно вашому улюбленцю',
    ('services', 'header_lead'): 'Повний перелік послуг клініки з детальним описом.',
    ('services', 'header_section_visible'): '1',
    ('doctors', 'header_tag'): 'Команда',
    ('doctors', 'header_title'): 'Лікарі, яким довіряють',
    ('doctors', 'header_lead'): (
        'Наші лікарі працюють за актуальними міжнародними протоколами, '
        'а сучасне діагностичне обладнання дозволяє виявляти захворювання на ранніх стадіях.'
    ),
    ('doctors', 'header_section_visible'): '1',
    ('contacts', 'header_tag'): 'Контакти',
    ('contacts', 'header_title'): 'Звʼяжіться з нами',
    ('contacts', 'header_lead'): 'Адреса, телефони та форма звернення.',
    ('contacts', 'header_section_visible'): '1',
    ('contacts', 'clinic_block_title'): 'Клініка',
    ('contacts', 'clinic_section_visible'): '1',
    ('contacts', 'form_block_title'): 'Написати нам',
    ('contacts', 'form_section_visible'): '1',
    ('contacts', 'map_section_visible'): '1',
    ('site', 'trust_strip_section_visible'): '1',
    ('site', 'footer_instagram_url'): '#',
    ('site', 'footer_telegram_url'): '#',
    ('site', 'footer_social_section_visible'): '1',
}

BLOCK_CONTENT_TYPES: dict[tuple[str, str], str] = {
    ('home', 'hero_image'): 'image',
}

MULTILINE_KEYS: frozenset[str] = frozenset({
    'hero_lead',
    'doctors_preview_note',
    'header_lead',
})

INLINE_KEYS: frozenset[str] = frozenset({
    'hero_title',
    'hero_cta_booking',
    'hero_cta_suffix',
    'hero_cta_phone',
    'hero_image_alt',
    'hero_stat_number',
    'hero_stat_label',
    'advantages_section_title',
    'services_preview_tag',
    'services_preview_title',
    'services_preview_hint',
    'services_preview_more_label',
    'doctors_preview_tag',
    'doctors_preview_title',
    'header_tag',
    'header_title',
    'clinic_block_title',
    'form_block_title',
    'footer_instagram_url',
    'footer_telegram_url',
})

VISIBILITY_SUFFIX = '_section_visible'


def is_visibility_key(key: str) -> bool:
    return key.endswith('_visible')
