# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
# # Copyright (C) 2012 Calthorpe Associates
# 
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3 of the License.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
# 
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates.
# Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709.
# Phone: (510) 548-6800. Web: www.calthorpe.com

# Django settings for analyser project.
import os
import sys
import datetime

SOCKETIO_HOST = '0.0.0.0'
SOCKETIO_PORT = '8000'

# Set this to the client key in local_settings to configure the system for the specified client
CLIENT = 'default'
# This is used so that public tables specific to all clients are created by South
# This allows us to have a single migration path across deployments (see models/__init__.py)
ALL_CLIENTS = ['sacog', 'scag', 'demo']

DEBUG = False
TEMPLATE_DEBUG = DEBUG

USE_SAMPLE_DATA_SETS = True

# Set the source for built form imports, or don't import them at all
IMPORT_BUILT_FORMS = 'JSON' #  set to 'CSV' to run full import, 'JSON' to use fixtures, or 'FALSE' to skip import
# Skip slow calculations for testing
SKIP_ALL_BUILT_FORMS = False
TEST_SKIP_BUILT_FORM_COMPUTATIONS = False
# Attempts to import features from the 'import' database
EXTERNALLY_IMPORT_FEATURES = True

# Enables or disables geoserver. Disabling it speeds up tests
# The current tastypie API version
API_VERSION = 1
API_PATH = "/footprint/api/v{0}".format(API_VERSION)

PROJECT_ROOT = os.path.dirname(__file__)
ROOT_PATH = os.path.dirname(__file__)

IMPORT_BASE_FEATURE = False

LOG_FILE = os.path.join(ROOT_PATH, 'debug.log')

ADMINS = (
    ('Andy Likuski', 'andy@calthorpe.com'),
    ('Evan Babb', 'evan@calthorpe.com'),
    ('Nick Wilson', 'nick@calthorpe.com'),
)

LOGIN_REDIRECT_URL = '/footprint'

MANAGERS = ADMINS

POSTGIS_VERSION = (1, 5, 3)
#POSTGIS_SQL_PATH = '/usr/share/postgresql/9.1/contrib/postgis-1.5/'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gis_django',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'import': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gis_django',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
CALTHORPE_ENGINE_PATH = os.path.join(ROOT_PATH, 'engines')

TIME_ZONE = 'America/Los_Angeles'
USE_TZ = True
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
DEFAULT_CHARSET = 'utf-8'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
# If you set this to False, Django will not format dates, numbers and # calendars according to the current locale
USE_L10N = True

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.DefaultStorageFinder",
)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/srv/calthorpe_media'

# This is used for the development server, only when DEBUG = True
STATIC_DOC_ROOT = MEDIA_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

TEMP_DIR = '/tmp/'

STATIC_ROOT = '/srv/calthorpe_static'

ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$z7yrc#(il44#+y8y2gwfv8g8u%b+gx!pv16q9%@5l=jl9zx6p'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'reversion.middleware.RevisionMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.static",

)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = os.path.basename(ROOT_PATH) + '.urls'

TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, 'templates'),
    os.path.join(ROOT_PATH, 'footprint/templates')
)

FOOTPRINT_TEMPLATE_DIR = os.path.join(ROOT_PATH, "footprint/templates/footprint")

FIXTURE_DIRS = (
    os.path.join(ROOT_PATH, 'fixtures'),
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

DJANGO_APPS = (
    'django.contrib.webdesign',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.gis',
)

THIRD_PARTY_APPS = (
    'django_extensions',
    'draft',  # draft must be listed before grapelli to enable admin form functionality
    'reversion',
    'reversion_compare',
    'grappelli',  # needs to be before admin
    'django.contrib.admin',
    'django.contrib.admindocs',
    'djcelery',
    'south',
    'jsonify',
    'django',
    'PIL',
    'ModestMaps',
    'TileStache',
    'memcache',
    'shapely',
    'tastypie',
    'behave',
    'picklefield',
    'django_nose',
    'geojson',
    'django_jenkins',
    'gunicorn',
    'datatools',
    'sendfile',
)

PROJECT_APPS = (
    'calthorpe',
    'footprint',
    'common',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',  # select one django or
    #'django_jenkins.tasks.dir_tests'      # directory tests discovery
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
    #'django_jenkins.tasks.run_jslint',
    #'django_jenkins.tasks.run_csslint',
    'django_jenkins.tasks.run_sloccount',
    #'django_jenkins.tasks.lettuce_tests',
    'django_jenkins.tasks.run_pylint',
)

GRAPPELLI_ADMIN_TITLE = "UrbanFootprint - Administration. (<a href=\"/footprint\">Back to Analysis)</a>"

CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
INTERNAL_IPS = ('127.0.0.1',)

# This is the official geojson way of specifying srids. Just insert the SRID in the {0}
SRID_PREFIX = 'urn:ogc:def:crs:EPSG::{0}'
DEFAULT_SRID = 4326  # X/Y values, as opposed to Spherical Mercator (EPSG:900913 or 3857) which is meters
# These are the bounds used for 4326, since the project extends infinitely toward the poles
DEFAULT_SRID_BOUNDS = [-20037508.34, -20037508.34, 20037508.34, 20037508.34]

SERIALIZATION_MODULES = {
    'json': 'wadofstuff.django.serializers.json'
}

import djcelery

djcelery.setup_loader()

# Here we define the default paths that UrbanFootprint will use during installation and stuff
CALTHORPE_ENGINE_PATH = '/srv/calthorpe/urbanfootprint/calthorpe/engines'

CALTHORPE_DATA_DUMP_LOCATION = '/srv/datadump'

SENDFILE_ROOT = MEDIA_ROOT + "/downloadable"

SENDFILE_URL = '/downloads/'
# if you wanted to exclude a folder, add "--exclude 'public/cache/*'"
CALTHORPE_DAILY_DUMP_RSYNC_EXTRA_PARAMS = ''

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
            #'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'INFO',
        },
        'django.db.backends': {
            'handlers': ['null'],  # Quiet by default!
            'propagate': False,
            'level': 'DEBUG',
        },
    }
}

if DEBUG:
    SENDFILE_BACKEND = 'sendfile.backends.development'
else:
    SENDFILE_BACKEND = 'sendfile.backends.nginx'

DOWNLOAD_FILE_EXPIRY = datetime.timedelta(days=1)

#celery generic
CELERY_TASK_RESULT_EXPIRES = 18000  # 5 hours.
CELERY_RESULT_PERSISTENT = True

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'run_cleanup_database': {
        'task': 'footprint.tasks.cleanup_export_job',
        'schedule': crontab(minute='0,20,40'),
        'args': (),
        'kwargs': {'fail_silently': True},
    },
}

try:
    from local_settings import *
except ImportError:
    print "WARNING: no local settings found for this project"

CELERY_TIMEZONE = TIME_ZONE
SQL_PATH = os.path.join(STATIC_ROOT, 'sql')

PATH_CONFIGURATIONS = {
    'default': dict(
        ROOT='/srv/',
        GIT_ROOT='/srv/calthorpe',
        BASE_PATH='/srv/calthorpe/urbanfootprint/calthorpe',
        PYTHON_INTERPRETER='/srv/calthorpe_env/bin/python',
        SERVER_ROOT='/srv/calthorpe/urbanfootprint/calthorpe/server',
        PROJ_ROOT='/srv/calthorpe/urbanfootprint/calthorpe/server/calthorpe/',
        WEBSOCKETS_ROOT='/srv/calthorpe/urbanfootprint/calthorpe/server/calthorpe/calthorpe_websockets',
    ),
    'jenkins': dict(
        ROOT='/var/lib/jenkins/jobs/FootprintTests/workspace',
        GIT_ROOT='/var/lib/jenkins/jobs/FootprintTests/workspace',
        BASE_PATH='/var/lib/jenkins/jobs/FootprintTests/workspace/calthorpe',
        PYTHON_INTERPRETER='/var/lib/jenkins/jobs/FootprintTests/workspace/calthorpe_ve/bin/python',
        SERVER_ROOT='/var/lib/jenkins/jobs/FootprintTests/workspace/calthorpe/server',
        PROJ_ROOT='/var/lib/jenkins/jobs/FootprintTests/workspace/calthorpe/server/calthorpe',
        WEBSOCKETS_ROOT='/var/lib/jenkins/jobs/FootprintTests/workspace/calthorpe/server/calthorpe_websockets'
    )

}
