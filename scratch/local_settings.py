#####################################
########## Django settings ##########
#####################################
# See <https://docs.djangoproject.com/en/1.11/ref/settings/>
# for more info and help. If you are stuck, you can try Googling about
# Django - many of these settings below have external documentation about them.
#
# The settings listed here are of special interest in configuring the site.

# SECURITY WARNING: keep the secret key used in production secret!
# You may use <http://www.miniwebtool.com/django-secret-key-generator/>
# to generate this key
# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True  # Change to False once you are done with runserver testing.

# Uncomment and set to the domain names this site is intended to serve.
# You must do this once you set DEBUG to False.
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
       'http://localhost:3000',
)
CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_SAMESITE=False
SESSION_COOKIE_SAMESITE=False
SESSION_COOKIE_SAMESITE = 'Strict'
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'WWW-Authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'X-Amz-Date',
    'access-control-allow-origin'
]


INSTALLED_APPS += (
    
)

# Caching. You can use memcached or redis instead.
# Documentation: <https://docs.djangoproject.com/en/1.11/topics/cache/>
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}


# Documentation: <https://docs.djangoproject.com/en/1.11/ref/databases/>
DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'letscode',
        'USER': 'letscode',
        'PASSWORD': 'password',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'sql_mode': 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION',
        },
    }
}

# Sessions.
# Documentation: <https://docs.djangoproject.com/en/1.11/topics/http/sessions/>
#SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Internationalization.
# Documentation: <https://docs.djangoproject.com/en/1.11/topics/i18n/>
LANGUAGE_CODE = 'en-ca'
DEFAULT_USER_TIME_ZONE = 'America/Toronto'
USE_I18N = True
USE_L10N = True
USE_TZ = True

## django-compressor settings, for speeding up page load times by minifying CSS and JavaScript files.
# Documentation: https://django-compressor.readthedocs.io/en/latest/
# COMPRESS_OUTPUT_DIR = 'cache'
# COMPRESS_CSS_FILTERS = [
#     'compressor.filters.css_default.CssAbsoluteFilter',
#     'compressor.filters.cssmin.CSSMinFilter',
# ]
# COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']
# COMPRESS_STORAGE = 'compressor.storage.GzipCompressorFileStorage'
# STATICFILES_FINDERS = ('compressor.finders.CompressorFinder',)


#########################################
########## Email configuration ##########
#########################################
# See <https://docs.djangoproject.com/en/1.11/topics/email/#email-backends>
# for more documentation. You should follow the information there to define 
# your email settings.

# Use this if you are just testing.
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# The following block is included for your convenience, if you want 
# to use Gmail.
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_HOST_USER = 'example@gmail.com'
#EMAIL_HOST_PASSWORD = '''password'''
#EMAIL_PORT = 587

# To use Mailgun, uncomment this block.
# You will need to run `pip install django-mailgun` for to get `MailgunBackend`.
#EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
#MAILGUN_ACCESS_KEY = '<your Mailgun access key>'
#MAILGUN_SERVER_NAME = '<your Mailgun domain>'

# You can also use Sendgrid, with `pip install sendgrid-django`.
#EMAIL_BACKEND = 'sgbackend.SendGridBackend'
#SENDGRID_API_KEY = '<Your SendGrid API Key>'

# if configured as shown below.

# A tuple of (name, email) pairs that specifies those who will be mailed
# when the server experiences an error when DEBUG = False.
ADMINS = (
    ('diwakargupta815', 'diwakargupta815.gmail.com'),
)

# The sender for the aforementioned emails.
# SERVER_EMAIL = 'Modern Online Judge'


##################################################
########### Static files configuration. ##########
##################################################
# See <https://docs.djangoproject.com/en/1.11/howto/static-files/>.

# Change this to somewhere more permanent., especially if you are using a 
# webserver to serve the static files. This is the directory where all the 
# You must configure your webserver to serve this directory as /static/ in production.
STATIC_ROOT = 'static/'

# URL to access static files.
STATIC_URL = '/static/'

# Uncomment to use hashed filenames with the cache framework.
#STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

############################################
############################################

SITE_NAME = 'Coder'
SITE_LONG_NAME = 'Coder: Club'
SITE_ADMIN_EMAIL = 'admin@example.com'
TERMS_OF_SERVICE_URL = ''

## Bridge controls.
# The judge connection address and port; where the judges will connect to the site.
# You should change this to something your judges can actually connect to 
# (e.g., a port that is unused and unblocked by a firewall).
BRIDGED_JUDGE_ADDRESS = [('localhost', 9999)]

# The bridged daemon bind address and port to communicate with the site.
#BRIDGED_DJANGO_ADDRESS = [('localhost', 9998)]

# Set to True to enable full-text searching for problems.
ENABLE_FTS = False

# Set of email providers to ban when a user registers, e.g., {'throwawaymail.com'}.
BAD_MAIL_PROVIDERS = set()

# The number of submissions that a staff user can rejudge at once without
# requiring the permission 'Rejudge a lot of submissions'.
# Uncomment to change the submission limit.
#SUBMISSIONS_REJUDGE_LIMIT = 10

## Event server.
# Uncomment to enable live updating.
#EVENT_DAEMON_USE = True

# Uncomment this section to use websocket/daemon.js included in the site.
EVENT_DAEMON_POST = 'ws://codeclub.com/15101'

# If you are using the defaults from the guide, it is this:
#EVENT_DAEMON_POST = 'ws://127.0.0.1:15101/'

# These are the publicly accessed interface configurations.
# They should match those used by the script.
#EVENT_DAEMON_GET = '<public ws:// URL for clients>'
#EVENT_DAEMON_GET_SSL = '<public wss:// URL for clients>'
#EVENT_DAEMON_POLL = '<public URL to access the HTTP long polling of event server>'
# i.e. the path to /channels/ exposed by the daemon, through whatever proxy setup you have.

# Using our standard nginx configuration, these should be.
EVENT_DAEMON_GET = 'ws://codeclub.com//event/'
#EVENT_DAEMON_GET_SSL = 'wss://<your domain>/event/' # Optional
EVENT_DAEMON_POLL = '/channels/'

# If you would like to use the AMQP-based event server from <https://github.com/*/event-server>,
# uncomment this section instead. This is more involved, and recommended to be done
# only after you have a working event server.
#EVENT_DAEMON_AMQP = '<amqp:// URL to connect to, including username and password>'
#EVENT_DAEMON_AMQP_EXCHANGE = '<AMQP exchange to use>'

## Celery
#CELERY_BROKER_URL = 'redis://localhost:6379'
#CELERY_RESULT_BACKEND = 'redis://localhost:6379'

## CDN control.
# Base URL for a copy of ace editor.
# Should contain ace.js, along with mode-*.js.
ACE_URL = '//cdnjs.cloudflare.com/ajax/libs/ace/1.2.3/'
JQUERY_JS = '//cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js'
SELECT2_JS_URL = '//cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/js/select2.min.js'
SELECT2_CSS_URL = '//cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/css/select2.min.css'

# A map of Earth in Equirectangular projection, for timezone selection.
# Please try not to hotlink this poor site.
TIMEZONE_MAP = 'http://naturalearth.springercarto.com/ne3_data/8192/textures/3_no_ice_clouds_8k.jpg'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'file': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {
        # You may use this handler as example for logging to other files..
        'bridge': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/bridge.log',
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'file',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'file',
        },
    },
    'loggers': {
        # Site 500 error mails.
        # 'django.request': {
        #     'handlers': ['mail_admins'],
        #     'level': 'ERROR',
        #     'propagate': False,
        # },
        # Judging logs as received by bridged.
        'judge.bridge': {
            'handlers': ['bridge', ],#'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        # Catch all log to stderr.
        '': {
            'handlers': ['console'],
        },
        # Other loggers of interest. Configure at will.
        #  - judge.user: logs naughty user behaviours.
        #  - judge.problem.pdf: PDF generation log.
        #  - judge.html: HTML parsing errors when processing problem statements etc.
        #  - judge.mail.activate: logs for the reply to activate feature.
        #  - event_socket_server
    },
}

## ======== Integration Settings ========
## Python Social Auth
# Documentation: https://python-social-auth.readthedocs.io/en/latest/
# You can define these to enable authentication through the following services.
SOCIAL_AUTH_GOOGLE_OAUTH2_CLIENT_ID = '*'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''
#SOCIAL_AUTH_FACEBOOK_KEY = ''
#SOCIAL_AUTH_FACEBOOK_SECRET = ''
#SOCIAL_AUTH_GITHUB_SECURE_KEY = ''
#SOCIAL_AUTH_GITHUB_SECURE_SECRET = ''
#SOCIAL_AUTH_DROPBOX_OAUTH2_KEY = ''
#SOCIAL_AUTH_DROPBOX_OAUTH2_SECRET = ''

## ======== Custom Configuration ========
# You may add whatever django configuration you would like here.
# Do try to keep it separate so you can quickly patch in new settings.
