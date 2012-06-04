# Django settings for tracklist project.

DEFAULT_FROM_EMAIL = 'Trackpattern <trackpattern-noreply@trackpattern.com>'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'moe@trackpattern.com'
EMAIL_HOST_PASSWORD = 'bl1tz5590'
EMAIL_PORT = 587

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
# ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tracklistdb', # Or path to database file if using sqlite3.
        'USER': 'tracklist', # Not used with sqlite3.
        'PASSWORD': 'tr4cklist', # Not used with sqlite3.
        'HOST': 'localhost', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/srv/tracklist/static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'
ADMIN_MEDIA_ROOT = '/srv/tracklist/static/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '%^u9q+24yy+7@)86%t3)zer4j5uxb(cqk)2(b30b)x58!8x160'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    "middleware.SubdomainMiddleware"
    )

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/home/'
ROOT_URLCONF = 'urls'
AUTH_PROFILE_MODULE = 'core.UserProfile'
AUTHENTICATION_BACKENDS = (
    'backends.TracklistAuthBackend',
    )

# Paging settings
DEFAULT_PAGESIZE = 10

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/srv/tracklist/templates/',
    '/srv/tracklist/csvimporter/templates/',
    '/srv/tracklist/static/landing/',
    )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    #    'django.contrib.messages',
    'home',
    'core',
    'csvimporter',

    # Uncomment the next line to enable the admin:
    'django.contrib.admin'
    )
SESSION_COOKIE_DOMAIN = 'trackpattern.com'
#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': True,
#    'formatters': {
#        'standard': {
#            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
#        },
#        },
#    'handlers': {
#        'default': {
#            'level':'DEBUG',
#            'class':'logging.handlers.RotatingFileHandler',
#            'filename': '/root/tracklist-logs/logs/default.log',
#            'maxBytes': 1024*1024*20, # 5 MB
#            'backupCount': 10,
#            'formatter':'standard',
#            },
#        'request_handler': {
#            'level':'DEBUG',
#            'class':'logging.handlers.RotatingFileHandler',
#            'filename': '/root/tracklist-logs/logs/django_request.log',
#            'maxBytes': 1024*1024*5, # 5 MB
#            'backupCount': 5,
#            'formatter':'standard',
#            },
#        'app': {
#            'level':'DEBUG',
#            'class':'logging.handlers.RotatingFileHandler',
#            'filename': '/root/tracklist-logs/logs/app.log',
#            'maxBytes': 1024*1024*5, # 5 MB
#            'backupCount': 5,
#            'formatter':'standard',
#            }
#        },
#    'loggers': {
#
#        '': {
#            'handlers': ['default'],
#            'level': 'DEBUG',
#            'propagate': True
#        },
#        'applog': {
#            'handlers': ['app'],
#            'level': 'DEBUG',
#            'propagate': True
#        },
#        'django.request': { # Stop SQL debug from logging to main logger
#                            'handlers': ['request_handler'],
#                            'level': 'DEBUG',
#                            'propagate': False
#        },
#        }
#}
