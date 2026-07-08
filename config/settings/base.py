from pathlib import Path

from decouple import config
from django.conf import settings as django_settings
from django.templatetags.static import static
from django.urls import reverse_lazy

from core.site_content_registry import build_content_sidebar_navigation

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def versioned_static(path: str) -> str:
    url = static(path)
    version = django_settings.STATIC_ASSET_VERSION
    separator = '&' if '?' in url else '?'
    return f'{url}{separator}v={version}'

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='127.0.0.1,localhost',
    cast=lambda v: [s.strip() for s in v.split(',') if s.strip()],
)

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'django_htmx',
    'csp',
    'core',
    'clinic',
    'bookings',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_settings',
                'core.context_processors.static_asset_version',
                'core.context_processors.navigation',
                'bookings.context_processors.callback_modal',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

_db_url = config('DATABASE_URL', default='')
if _db_url:
    import dj_database_url

    DATABASES = {
        'default': dj_database_url.parse(_db_url, conn_max_age=600),
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'uk'
TIME_ZONE = 'Europe/Kyiv'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [BASE_DIR / 'locale']

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_ASSET_VERSION = config('STATIC_ASSET_VERSION', default='20260708i')
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {'handlers': ['console'], 'level': 'WARNING'},
    'loggers': {
        'core': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'clinic': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'bookings': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'django': {'handlers': ['console'], 'level': 'WARNING', 'propagate': False},
    },
}

CONTENT_SECURITY_POLICY = {
    'EXCLUDE_URL_PREFIXES': ('/admin/',),
    'DIRECTIVES': {
        'default-src': ("'self'",),
        'script-src': ("'self'",),
        'style-src': ("'self'", 'https://fonts.googleapis.com'),
        'font-src': ("'self'", 'https://fonts.gstatic.com'),
        'img-src': ("'self'", 'data:'),
        'connect-src': ("'self'",),
        'frame-src': ("'self'", 'https://www.google.com', 'https://maps.google.com'),
        'frame-ancestors': ("'none'",),
        'base-uri': ("'self'",),
        'form-action': ("'self'",),
    },
}

TINYMCE_DEFAULT_CONFIG = {
    'menubar': False,
    'plugins': 'autoresize link lists image code',
    'toolbar': 'undo redo | bold italic underline | bullist numlist | link image | code',
    'min_height': 120,
    'max_height': 560,
    'autoresize_bottom_margin': 12,
    'resize': False,
    'content_css': False,
    'skin': 'oxide',
}

UNFOLD = {
    'SITE_TITLE': 'Адмін панель Фенікс',
    'SITE_HEADER': 'Адмін панель Фенікс',
    'SITE_SYMBOL': None,
    'BORDER_RADIUS': '10px',
    'SITE_ICON': {
        'light': lambda request: versioned_static('images/brand-icon.png'),
        'dark': lambda request: versioned_static('images/brand-icon.png'),
    },
    'SITE_FAVICONS': [
        {
            'rel': 'icon',
            'sizes': 'any',
            'href': lambda request: versioned_static('images/favicon.ico'),
        },
        {
            'rel': 'icon',
            'type': 'image/png',
            'sizes': '32x32',
            'href': lambda request: versioned_static('images/favicon-32.png'),
        },
        {
            'rel': 'icon',
            'type': 'image/png',
            'sizes': '16x16',
            'href': lambda request: versioned_static('images/favicon-16.png'),
        },
        {
            'rel': 'apple-touch-icon',
            'sizes': '180x180',
            'href': lambda request: versioned_static('images/apple-touch-icon.png'),
        },
    ],
    'SIDEBAR': {
        'show_search': True,
        'command_search': True,
        'show_all_applications': False,
        'navigation': [
            {
                'title': 'Налаштування',
                'separator': False,
                'items': [
                    {
                        'title': 'Налаштування сайту',
                        'icon': 'settings',
                        'link': reverse_lazy('admin:core_sitesettings_changelist'),
                    },
                ],
            },
            *build_content_sidebar_navigation(),
            {
                'title': 'Контент',
                'separator': True,
                'items': [
                    {
                        'title': 'Послуги',
                        'icon': 'medical_services',
                        'link': reverse_lazy('admin:clinic_service_changelist'),
                    },
                    {
                        'title': 'Лікарі',
                        'icon': 'person',
                        'link': reverse_lazy('admin:clinic_doctor_changelist'),
                    },
                    {
                        'title': 'Переваги',
                        'icon': 'star',
                        'link': reverse_lazy('admin:clinic_advantage_changelist'),
                    },
                ],
            },
            {
                'title': 'Заявки клієнтів',
                'separator': True,
                'items': [
                    {
                        'title': 'Заявки на запис',
                        'icon': 'calendar_today',
                        'link': reverse_lazy('admin:bookings_appointmentrequest_changelist'),
                    },
                    {
                        'title': 'Запити на передзвінок',
                        'icon': 'phone_callback',
                        'link': reverse_lazy('admin:bookings_callbacklead_changelist'),
                    },
                    {
                        'title': 'Звернення з контактів',
                        'icon': 'mail',
                        'link': reverse_lazy('admin:clinic_contactmessage_changelist'),
                    },
                ],
            },
        ],
    },
    'COLORS': {
        'primary': {
            '50': '#FFF6F1',
            '100': '#FFE4D6',
            '200': '#FFC9AD',
            '300': '#FFA57A',
            '400': '#FF8F5E',
            '500': '#FF7A45',
            '600': '#E86632',
            '700': '#C95524',
            '800': '#A3441C',
            '900': '#7D3315',
            '950': '#5A2410',
        },
    },
}

PET_TYPE_CHOICES = [
    ('dog', 'Собака'),
    ('cat', 'Кіт'),
    ('rabbit', 'Кролик'),
    ('rodent', 'Гризун'),
    ('bird', 'Птах'),
    ('other', 'Інше'),
]

BOOKING_TIME_SLOTS = [
    '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
    '12:00', '12:30', '13:00', '14:00', '14:30', '15:00',
    '15:30', '16:00', '16:30', '17:00', '17:30', '18:00',
]
