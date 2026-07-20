from django.db import migrations

SERVICES = [
    {
        'slug': 'surgery',
        'name': 'Хірургія',
        'short_description': 'Планові та екстрені операції',
        'full_description': (
            'Хірургічне лікування будь-якої складності: від мʼяких тканин до ортопедії. '
            'Сучасна операційна, безпечний наркоз і післяопераційний догляд.'
        ),
        'icon': 'scissors',
        'bullets': ['Передопераційна діагностика', 'Безпечний наркоз', 'Сучасна операційна', 'Післяопераційний догляд'],
        'is_urgent': False,
        'order': 1,
    },
    {
        'slug': 'therapy',
        'name': 'Терапія',
        'short_description': 'Огляд та лікування',
        'full_description': (
            'Первинний огляд, діагностика гострих та хронічних захворювань, '
            'складання плану лікування та спостереження за станом тварини.'
        ),
        'icon': 'stethoscope',
        'bullets': ['Огляд лікаря', 'Діагностика на місці', 'План лікування', 'Контрольний візит'],
        'is_urgent': False,
        'order': 2,
    },
    {
        'slug': 'intensive',
        'name': 'Інтенсивна терапія',
        'short_description': 'Цілодобовий стаціонар',
        'full_description': (
            'Власний цілодобовий стаціонар інтенсивної терапії та реанімації. '
            'Постійний моніторинг стану пацієнта у критичні періоди.'
        ),
        'icon': 'stethoscope',
        'bullets': ['Цілодобовий нагляд', 'Реанімація', 'Моніторинг стану', 'Інфузійна терапія'],
        'is_urgent': True,
        'order': 3,
    },
    {
        'slug': 'dental',
        'name': 'Стоматологія',
        'short_description': 'Чистка та лікування зубів',
        'full_description': (
            'Ультразвукова чистка, лікування та видалення зубів, '
            'стоматологічні процедури під легким наркозом.'
        ),
        'icon': 'tooth',
        'bullets': ['Ультразвукова чистка', 'Лікування зубів', 'Видалення', 'Контроль ясен'],
        'is_urgent': False,
        'order': 4,
    },
    {
        'slug': 'visual-diag',
        'name': 'Візуальна діагностика',
        'short_description': 'УЗД, рентген',
        'full_description': (
            'Ультразвукова діагностика, цифровий рентген та інші методи візуалізації '
            'для точного виявлення захворювань.'
        ),
        'icon': 'scan',
        'bullets': ['УЗД', 'Цифровий рентген', 'Ехокардіографія', 'Результати у день звернення'],
        'is_urgent': False,
        'order': 5,
    },
    {
        'slug': 'endoscopy',
        'name': 'Ендоскопія',
        'short_description': 'Внутрішній огляд',
        'full_description': (
            'Ендоскопічне дослідження органів шлунково-кишкового тракту та дихальних шляхів '
            'для точної діагностики без оперативного втручання.'
        ),
        'icon': 'scan',
        'bullets': ['Гастроскопія', 'Отоскопія', 'Ріноскопія', 'Бронхоскопія', 'Мінімально інвазивно'],
        'is_urgent': False,
        'order': 6,
    },
    {
        'slug': 'vaccine',
        'name': 'Вакцинація',
        'short_description': 'Щеплення та паспорт',
        'full_description': (
            'Комплексні щеплення для собак і котів. Вакцинація від сказу, '
            'ведення ветеринарного паспорта.'
        ),
        'icon': 'syringe',
        'bullets': ['Огляд перед щепленням', 'Сертифіковані вакцини', 'Запис у ветпаспорт', 'Нагадування про ревакцинацію'],
        'is_urgent': False,
        'order': 7,
    },
    {
        'slug': 'cardiology',
        'name': 'Кардіологія',
        'short_description': 'Діагностика серця',
        'full_description': (
            'Діагностика та лікування захворювань серцево-судинної системи. '
            'ЕКГ, ехокардіографія та моніторинг серцевої діяльності.'
        ),
        'icon': 'stethoscope',
        'bullets': ['ЕКГ', 'Ехокардіографія', 'Холтер-моніторинг', 'План лікування'],
        'is_urgent': False,
        'order': 8,
    },
    {
        'slug': 'laboratory',
        'name': 'Лабораторія',
        'short_description': 'Аналізи та дослідження',
        'full_description': (
            'Власна лабораторія: клінічні, біохімічні та спеціальні аналізи. '
            'Швидкі результати для оперативного прийняття рішень.'
        ),
        'icon': 'scan',
        'bullets': ['Клінічні аналізи', 'Біохімія крові', 'Цитологія', 'Результати у день звернення'],
        'is_urgent': False,
        'order': 9,
    },
    {
        'slug': 'endocrinology',
        'name': 'Ендокринологія',
        'short_description': 'Гормональні розлади',
        'full_description': (
            'Діагностика та лікування ендокринних захворювань: '
            'цукровий діабет, гіпотиреоз, синдром Кушинга та інші.'
        ),
        'icon': 'stethoscope',
        'bullets': ['Гормональні аналізи', 'Діагностика діабету', 'План терапії', 'Контроль стану'],
        'is_urgent': False,
        'order': 10,
    },
    {
        'slug': 'dermatology',
        'name': 'Дерматологія',
        'short_description': 'Шкіра та шерсть',
        'full_description': (
            'Діагностика та лікування захворювань шкіри, шерсті та кігтів. '
            'Алергії, дерматити, паразитарні ураження.'
        ),
        'icon': 'stethoscope',
        'bullets': ['Огляд шкіри', 'Дерматологічні дослідження', 'Алергологічні тести', 'План лікування'],
        'is_urgent': False,
        'order': 11,
    },
]

DOCTORS = [
    ('veronika-volodymyrivna', 'Вероніка Володимирівна', 'Цитолог, анестезіолог', 'ВВ'),
    ('oleksandra-serhiivna', 'Олександра Сергіївна', 'Кардіолог, анестезіолог', 'ОС'),
    ('anastasiia-volodymyrivna', 'Анастасія Володимирівна', 'Лікар-терапевт', 'АВ'),
    ('maksym-viktorovych', 'Максим Вікторович', 'Терапевт, дерматолог, онколог', 'МВ'),
    ('yelyzaveta-oleksandrivna', 'Єлизавета Олександрівна', 'Дерматолог', 'ЄО'),
    ('liliia-ivanivna', 'Лілія Іванівна', 'Терапевт, ендокринолог', 'ЛІ'),
    ('hryhorii-oleksandrovych', 'Григорій Олександрович', 'Ортопед, хірург', 'ГО'),
    ('hanna-oleksandrivna', 'Ганна Олександрівна', 'Хірург, терапевт, онколог', 'ГА'),
    ('daryna-serhiivna', 'Дарина Сергіївна', 'Терапевт, нефролог', 'ДС'),
    ('svitlana-serhiivna', 'Світлана Сергіївна', 'Стоматолог', 'СС'),
    ('kseniia-serhiivna', 'Ксенія Сергіївна', 'Візуальна діагностика, лабораторна діагностика', 'КС'),
    ('ivan-leonidovych', 'Іван Леонідович', 'Лікар-інфекціоніст', 'ІЛ'),
]

ADVANTAGES = [
    ('clock', 'Цілодобовий стаціонар', (
        'Завдяки власному стаціонару інтенсивної терапії ви можете бути впевнені: '
        'ваш улюбленець ніколи не залишиться без уваги у скрутну хвилину.'
    ), False),
    ('shield', 'Сучасне обладнання', (
        'Клініка забезпечена новітнім обладнанням, що допомагає у швидкій діагностиці пацієнтів.'
    ), False),
    ('star', 'Доказова медицина', (
        'Наші фахівці працюють за актуальними міжнародними протоколами, '
        'спираючись на доказову медицину.'
    ), False),
    ('heart', 'Навчання персоналу', (
        'Постійне навчання, поглиблення знань та навичок персоналу, '
        'використання сучасних методів діагностики.'
    ), True),
]

OLD_ADVANTAGES = [
    ('clock', 'Цілодобово', 'Працюємо 24/7 без вихідних', False),
    ('shield', 'Сучасне обладнання', 'УЗД, цифровий рентген, лабораторія', False),
    ('star', 'Кваліфіковані лікарі', 'Сертифікація, постійне навчання', False),
    ('heart', 'Турбота і увага', 'Спокійне середовище, без черг', True),
]

OLD_DOCTORS = [
    ('shevchuk', 'Олена Шевчук', 'Терапевт · Кардіолог', 'ОШ'),
    ('kovalenko', 'Андрій Коваленко', 'Хірург', 'АК'),
    ('lytvyn', 'Марія Литвин', 'Дерматолог', 'МЛ'),
    ('bilyk', 'Тарас Білик', 'Стоматолог', 'ТБ'),
]


def _upsert_services(Service):
    active_slugs = {item['slug'] for item in SERVICES}
    Service.objects.exclude(slug__in=active_slugs).update(is_active=False)
    for item in SERVICES:
        Service.objects.update_or_create(
            slug=item['slug'],
            defaults={
                **item,
                'price_hint': '',
                'is_active': True,
            },
        )


def _replace_doctors(Doctor):
    Doctor.objects.all().delete()
    for order, (slug, name, specialization, initials) in enumerate(DOCTORS, start=1):
        Doctor.objects.create(
            slug=slug,
            name=name,
            specialization=specialization,
            experience_years=5,
            initials=initials,
            photo='',
            rating='4.9',
            patients_label='',
            bio='',
            order=order,
            is_active=True,
        )


def _update_advantages(Advantage, data):
    for order, (icon, title, description, is_alt) in enumerate(data, start=1):
        adv = Advantage.objects.filter(order=order).first()
        if adv:
            adv.icon = icon
            adv.title = title
            adv.description = description
            adv.is_alt = is_alt
            adv.save()
        else:
            Advantage.objects.create(
                icon=icon,
                title=title,
                description=description,
                order=order,
                is_alt=is_alt,
            )


def forwards(apps, schema_editor):
    Service = apps.get_model('clinic', 'Service')
    Doctor = apps.get_model('clinic', 'Doctor')
    Advantage = apps.get_model('clinic', 'Advantage')
    _upsert_services(Service)
    _replace_doctors(Doctor)
    _update_advantages(Advantage, ADVANTAGES)


def backwards(apps, schema_editor):
    Service = apps.get_model('clinic', 'Service')
    Doctor = apps.get_model('clinic', 'Doctor')
    Advantage = apps.get_model('clinic', 'Advantage')

    Service.objects.filter(slug='online').update(is_active=True)
    Service.objects.exclude(
        slug__in=['therapy', 'vaccine', 'surgery', 'diag', 'dental', 'online'],
    ).update(is_active=False)

    diag = Service.objects.filter(slug='visual-diag').first()
    if diag:
        diag.slug = 'diag'
        diag.name = 'Діагностика'
        diag.short_description = 'УЗД, рентген, аналізи'
        diag.save()

    Doctor.objects.all().delete()
    for order, (slug, name, specialization, initials) in enumerate(OLD_DOCTORS, start=1):
        Doctor.objects.create(
            slug=slug,
            name=name,
            specialization=specialization,
            experience_years=10,
            initials=initials,
            photo='',
            rating='4.9',
            patients_label='1000+ пацієнтів',
            bio='',
            order=order,
            is_active=True,
        )

    _update_advantages(Advantage, OLD_ADVANTAGES)


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0005_replace_ambulance_with_online'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
