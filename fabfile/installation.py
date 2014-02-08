# UrbanFootprint-California, Scenario Planning Model
# 
# Copyright (C) 2012-2013 Calthorpe Associates
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
# Contact: Calthorpe Associates (urbanfootprint@calthorpe.com)
# Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709.
# Phone: (510) 548-6800.      Web: www.calthorpe.com
# 

#
#import fabric
import os
import sys

# Need to append the sys path to make the fabric django contrib module work. Sadly these things must
# be done in this order to have the django_settings object available
from fabric.context_managers import shell_env

from fabric.contrib import django

django.settings_module('footprint.settings')

from django.conf import settings as django_settings
from django.core.management import call_command

import cuisine
from cuisine_postgresql import (postgresql_role_ensure, postgresql_database_ensure, run_as_postgres )
from fabric.api import (cd, run, env, settings, task)
from fabric.operations import sudo, local, prompt
from fabric.contrib import console
from fabric.contrib.files import append, exists, sed

from footprint.common.utils.postgres_utils import build_postgres_conn_string, postgres_env_password_loaded

PROJ_VER = '4.8.0'
GEOS_VER = '3.3.8'
GDAL_VER = '1.10.1'

PROJ_PATH = '/usr/local/proj/' + PROJ_VER
GEOS_PATH = '/usr/local/geos/' + GEOS_VER
GDAL_PATH = '/usr/local/gdal/' + GDAL_VER

FILEGDBAPI_FILE = 'FileGDB_API_1_3-64.tar.gz'
FILEGDBAPI_LOCATION = 'http://downloads2.esri.com/Software/%s' % (FILEGDBAPI_FILE,)

JAVA_VERSION = 'java-7-oracle'
JAVA_RESPOSITORY = 'ppa:webupd8team/java'

POSTGIS_PATH = '/usr/share/postgresql/9.1/contrib/postgis-1.5/'


def set_paths():
    global ROOT, GIT_ROOT, BASE_PATH, PROJ_ROOT, PYTHON_INTERPRETER, WEBSOCKETS_ROOT, SERVER_ROOT, TEMP_DIR

    if 'env' in globals():
        env = globals()['env']
    else:
        env = 'default'

    configuration = getattr(env, 'client', 'default')
    configurations = django_settings.PATH_CONFIGURATIONS
    if configuration in configurations:
        path_dict = configurations[configuration]
    else:
        path_dict = configurations['default']

    ROOT = path_dict['ROOT']
    GIT_ROOT = path_dict['GIT_ROOT']
    BASE_PATH = path_dict['BASE_PATH']
    PROJ_ROOT = path_dict['PROJ_ROOT']
    PYTHON_INTERPRETER = path_dict['PYTHON_INTERPRETER']
    WEBSOCKETS_ROOT = path_dict['WEBSOCKETS_ROOT']
    SERVER_ROOT = path_dict['SERVER_ROOT']

    TEMP_DIR = django_settings.TEMP_DIR

set_paths()

def virtualenv(command):
    sudo('source ' + env.virtualenv_directory + '/bin/activate && ' + command, user=env.deploy_user)


def manage_py(command):
    sudo(PYTHON_INTERPRETER + ' ' + SERVER_ROOT + '/manage.py ' + command, user=env.deploy_user)

@task
def setup_databases():

    # create production postgres database and test database
    # needs to match local_settings.py deployment values

    postgresql_role_ensure(env.deploy_user, env.password, superuser=True, createdb=True, createrole=True,
                           inherit=True, login=True)

    postgresql_database_ensure('urbanfootprint', owner=env.deploy_user, template='template_postgis')

    # the following two lines below should be enabled for postgis 2.0 (also remove template_postgis from above lines)
    #run_as_postgres('psql -U postgres -c "CREATE EXTENSION IF NOT EXISTS POSTGIS" urbanfootprint')


@task
def setup_node_env():
    with cd(WEBSOCKETS_ROOT):
        # removes this
        try:
            sudo('rm -r carto')
        except:
            pass
        run('npm install .')
        run('git clone git://github.com/mapbox/carto.git')
        # run('git clone https://github.com/mapbox/node-sqlite3.git')
        # rune('git clone https://github.com/mapbox/millstone.git')
        # sudo('npm install -g ./node-sqlite3')
        sudo('npm install -g ./carto')
        # sudo('npm install -g ./millstone')
        sudo('chown -R {0}.www-data node_modules/'.format(env.deploy_user))


@task
def setup_urbanfootprint(upgrade_env=True, erase=False):
    """
    Runs all the steps necessary to configure urbanfootprint
    """
    if erase:
        sudo('rm {git_root}* -rf'.format(git_root=GIT_ROOT))
    set_paths()
    print "ROOT = {0}\n".format(ROOT), \
        "GIT_ROOT = {0}\n".format(GIT_ROOT), \
        "BASE_PATH = {0}\n".format(BASE_PATH), \
        "PROJECT_PATH: {0}\n".format(PROJ_ROOT), \
        "WEBSOCKETS_ROOT: {0}\n".format(WEBSOCKETS_ROOT)


    from fabfile.management import deploy
    # Make sure deployment user exists and that the key is setup correctly
    cuisine.user_ensure(env.deploy_user)
    if env.user != env.deploy_user:
        sudo('chsh -s /bin/bash {0}'.format(env.deploy_user))
        sudo('mkdir -p ~{0}/.ssh/'.format(env.deploy_user), user=env.deploy_user)
        sudo('cp ~/.ssh/id_rsa* ~{0}/.ssh/'.format(env.deploy_user))
    sudo('chown {0}.{0} ~{0}/.ssh/id_rsa*'.format(env.deploy_user))
    sudo('chmod 600 ~{0}/.ssh/id_rsa'.format(env.deploy_user), user=env.deploy_user)

    # add UbuntuGIS repo
    sudo('add-apt-repository ppa:ubuntugis/ubuntugis-unstable -y')
    sudo('add-apt-repository ppa:chris-lea/node.js -y')
    sudo('add-apt-repository ppa:chris-lea/nginx-devel -y')

    cuisine.package_update()
    cuisine.package_upgrade()

    # using oracle's jdk for good compatibility
    # intentionally not install postgresql-9.1-postgis until we can upgrade to django 1.5.x and postgis 2.0
    cuisine.package_ensure(
        'build-essential openjdk-6-jre openjdk-6-jdk postgresql git python-software-properties proj libproj-dev '
        'python-pip python-virtualenv python-dev virtualenvwrapper postgresql-server-dev-9.1 '
        'gdal-bin libgdal1-dev nginx varnish supervisor redis-server curl python-gdal nodejs graphviz-dev graphviz'
        # 'libboost-dev libboost-filesystem-dev libboost-program-options-dev libboost-python-dev libboost-regex-dev '
        #     'libboost-system-dev libboost-thread-dev
    )

    #install older postgis
    create_template_postgis()

    cuisine.group_user_ensure("www-data", env.deploy_user)
    cuisine.group_user_ensure("sudo", env.deploy_user)

    # setup deployment user git settings #TODO: make more sense of this... probably shouldn't be this for all setups
    sudo('su {0} -c "git config --global user.email \"deploy@calthorpe.com\""'.format(env.deploy_user))
    sudo('su {0} -c "git config --global user.name \"Calthorpe Deployment\""'.format(env.deploy_user))

    # these directories should be owned by calthorpe and the www-data user
    dirs_to_create = [
        GIT_ROOT,
        '/srv/calthorpe_static',
        '/srv/calthorpe_media',
        '/srv/calthorpe_media/cartocss',
        '/srv/calthorpe_media/uploads',
        '/tmp/stache/'
    ]

    # create folders for calthorpe deployment
    for dir in dirs_to_create:
        sudo('mkdir -p {0}'.format(dir))
        sudo('chmod +t {0}'.format(dir))
        sudo('chown -R {user}.www-data {dir}'.format(dir=dir, user=env.deploy_user))

    sudo('chmod g+w -R /srv/calthorpe_media')

    #create virtualenv
    if not cuisine.dir_exists(env.virtualenv_directory):
        sudo("virtualenv {env}".format(env=env.virtualenv_directory))
        sudo('chown -R {user}.www-data {env}'.format(user=env.deploy_user, env=env.virtualenv_directory))

    install_mapnik()
    install_osgeo()
    # clone repo if needed
    if not cuisine.dir_exists(BASE_PATH):
        with cd(GIT_ROOT):
            sudo('su {0} -c "git clone git@bitbucket.org:calthorpe/urbanfootprint.git"'.format(env.deploy_user))
            sudo('chown -R {user}.www-data {BASE_PATH}/..'.format(user=env.deploy_user, BASE_PATH=BASE_PATH))
            with cd('urbanfootprint'):
                sudo('git submodule init')
                sudo('git submodule update')

    setup_databases()

    with cd(PROJ_ROOT):
        if not exists('local_settings.py'):
            sudo('ln -s local_settings.py.{CLIENT} local_settings.py'.format(CLIENT=env.client))

    setup_node_env()
    # update varnish default port
    #sed('/etc/default/varnish', r'^DAEMON_OPTS="-a :6081', 'DAEMON_OPTS="-a :80', use_sudo=True)

    # soft link all configuration files
    with cd('/etc/varnish'):
        sudo('rm -f default.vcl')
        #sudo('ln -s /srv/calthorpe/urbanfootprint/calthorpe/server/conf/etc/varnish/default.vcl.prod default.vcl')

    nginx_configure()

    with cd('/etc/supervisor/conf.d'):
        sudo('rm -f calthorpe.conf')
        # Link the appropriate supervisor config file. dev omits a web server, and the log files are different
        supervisor_conf_ext = 'dev' if env.dev else 'prod'

        link_supervisor_config_path = "ln -s {BASE_PATH}/conf/etc/supervisor/conf.d/calthorpe.supervisor.{supervisor_extension} calthorpe.conf"
        sudo(link_supervisor_config_path.format(BASE_PATH=BASE_PATH, supervisor_extension=supervisor_conf_ext))

    install_sproutcore()

    # trigger deploy to update virtualenv and restart services
    deploy(upgrade_env=upgrade_env)
    patch_django_layermapping()


@task
def setup_jenkins():
    """
    Runs all the steps necessary to configure Jenkins CI server
    """
    # removes previous versions of jenkins to prevent conflict
    sudo("apt-get remove --purge jenkins*")

    # add keys and latest/greatest debian repo from jenkins site
    # sudo('wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add -')
    # sudo('echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list')
    run('wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add -')
    sudo("echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list'")

    sudo('apt-get update')
    sudo('apt-get install jenkins --upgrade')

    # add jenkins user to the shadow group
    sudo('usermod -a -G shadow jenkins')

    # change jenkins default port to 9000apt-
    sed('/etc/default/jenkins', before='^HTTP_PORT=.*', after='HTTP_PORT=9000',
        backup='', use_sudo=True)

    sudo('service jenkins restart')

    #setup_urbanfootprint()
    # setup jenkins user git settingsls

    #sudo('su jenkins -c "git config --global user.email \"build@calthorpe.com\""')
    #sudo('su jenkins -c "git config --global user.name \"Calthorpe Build\""')

    # create folders for jenkin's Calthorpe-build job
    #sudo('mkdir -p /srv/jenkins')
    #sudo('chmod +t /srv/jenkins')alter
    #sudo('mkdir -p /srv/jenkins/static') # needs to match local_settings.py.jenkins value
    #sudo('mkdir -p /srv/jenkins/media') # needs to match local_settings.py.jenkins value
    #sudo('chown -R jenkins.www-data /srv/jenkins')

    # create jenkins' postgres database and test database
    postgresql_role_ensure('jenkins', 'JNKNZ', superuser=True, createdb=True, createrole=True,
                           inherit=True, login=True)

    #postgresql_database_ensure('jenkins', owner='jenkins')
    #run_as_postgres('psql -U postgres -c "CREATE EXTENSION IF NOT EXISTS POSTGIS" jenkins')

    #postgresql_database_ensure('test_jenkins', owner='jenkins')
    #run_as_postgres('psql -U postgres -c "CREATE EXTENSION IF NOT EXISTS POSTGIS" test_jenkins')


@task
def publish_datadump():
    """
    Generates a local datadump and publishes it to the requested servers
    """

    call_command('create_datadump')

    # Make sure remote folders exist
    sudo('mkdir -p {0}'.format(env.DATA_DUMP_PATH))
    sudo('chown -R {0}.www-data {1}'.format(env.user, env.DATA_DUMP_PATH))

    # rsync media files to remote server
    rsync_cmd = 'rsync --delete -rapthzv -e ssh'

    remote_server_conn_string = '{user}@{host}'.format(
        user=env.user,
        host=env.host_string)

    absolute_remote_data_dump_folder = '{remote_server_conn_string}:{data_dump_folder}'.format(
        remote_server_conn_string=remote_server_conn_string,
        data_dump_folder=env.DATA_DUMP_PATH)


    # rsync local media folder into remote data dump folder

    local('{rsync} {local_media_folder} {absolute_remote_data_dump_folder}/media'.format(
        rsync=rsync_cmd,
        absolute_remote_data_dump_folder=absolute_remote_data_dump_folder,
        local_media_folder=django_settings.MEDIA_ROOT))

    # rsync local postgres datadump file into remote data dump location

    local_dump_file = os.path.join(django_settings.CALTHORPE_DATA_DUMP_LOCATION, 'pg_dump.dmp')

    local('{rsync} {local_dump_file} {absolute_remote_data_dump_folder}/pg_dump.dmp '.format(
        rsync=rsync_cmd,
        absolute_remote_data_dump_folder=absolute_remote_data_dump_folder,
        local_dump_file=local_dump_file))


@task
def fetch_datadump(force_local_db_destroy=False, use_local=False):
    """
    Sync local database and media folder with official data_dump
    'fetch_datadump:force_local_db_destroy:True' to not prompt for db destruction confirmation
    'fetch_datadump:use_local:True avoid going through the ssh wire
    """

    db = django_settings.DATABASES['default']

    if not force_local_db_destroy:
        msg = 'You are DESTROYING the local "{dbname}" database! Continue?'.format(
            dbname=db['NAME'])

        accepted_database_destroy = console.confirm(msg, default=False)

        if not accepted_database_destroy:
            print 'Aborting fetch_datadump()'
            return

    rsync_cmd = 'rsync --delete -rapthzv -e ssh'

    if use_local:
        # it is a local grab, skip the fetching of resources across the wire

        absolute_remote_data_dump_folder = '{data_dump_folder}'.format(
            data_dump_folder=env.DATA_DUMP_PATH)

    else:
        # do remote grab
        remote_server_conn_string = '{user}@{host}'.format(
            user=env.user,
            host=env.host_string)

        absolute_remote_data_dump_folder = '{remote_server_conn_string}:{data_dump_folder}'.format(
            remote_server_conn_string=remote_server_conn_string,
            data_dump_folder=env.DATA_DUMP_PATH)

    # rsync remote media folder (or local dump folder) into local

    local('{rsync} {absolute_remote_data_dump_folder}/media {local_media_folder}'.format(
        rsync=rsync_cmd,
        absolute_remote_data_dump_folder=absolute_remote_data_dump_folder,
        local_media_folder=django_settings.MEDIA_ROOT))

    # rsync postgres datadump file into local folder
    # The reason we don't use tempfile.gettempdir() is that we always want the file to exist
    # in the same place so we can take advantage of rsync's delta file-chunk speedup. In OSX,
    # after every reboot, gettempdir returns a different directory defeating the point of using
    # rsync. We use the '/tmp/' folder instead

    local_dump_file = os.path.join(TEMP_DIR, 'pg_dump.dmp')

    local('{rsync} {absolute_remote_data_dump_folder}/pg_dump.dmp {local_dump_file}'.format(
        rsync=rsync_cmd,
        absolute_remote_data_dump_folder=absolute_remote_data_dump_folder,
        local_dump_file=local_dump_file))

    with postgres_env_password_loaded(db):
        db_conn_string = build_postgres_conn_string(db)

    # Some versions of postgres do not have --if-exists, so just ignore the error if it doesn't exist
        with settings(warn_only=True):
            local('dropdb {db_conn_string}'.format(db_conn_string=db_conn_string))

        local('createdb -O {db_user} {db_conn_string}'.format(db_user=db['USER'], db_conn_string=db_conn_string))

    # try to catch the typical error of not having the amigocloud role defined
        with settings(warn_only=True):
            result = local('pg_restore {db_conn_string} -d {dbname} {local_dump_file}'.format(
                db_conn_string=build_postgres_conn_string(db, omit_db=True),
                dbname=db['NAME'],
                local_dump_file=local_dump_file))

        if result.failed:
            print "ERROR: You probably don't have 'calthorpe' ROLE defined. Fix by executing:"
            print "CREATE ROLE calthorpe; GRANT calthorpe to {user};".format(user=db['USER'])

            raise SystemExit()


@task
def deploy_data():
    """
    Logs into remote machine and loads the data_load that has been published to the same machine
    """

    # stop any connections to the db
    with settings(warn_only=True):
        sudo('supervisorctl stop all')
        sudo('/etc/init.d/supervisor stop')

    with cd(PROJ_ROOT):
        fab_cmd = env.virtualenv_directory + '/bin/fab'
        sudo('{fab_cmd} localhost:skip_ssh=True fetch_datadump:use_local=True,force_local_db_destroy=True'.format(
            fab_cmd=fab_cmd), user=env.deploy_user)

    if os.path.exists('/srv/calthorpe_media'):
        sudo('rm -r /srv/calthorpe_media')
    sudo('cp -R /srv/datadump/media/calthorpe_media /srv/')
    directory_permissions()

    # start connections to the db
    sudo('/etc/init.d/supervisor start')
    sudo('supervisorctl start all')

@task
def directory_permissions():
    sudo('chown calthorpe:www-data /srv/calthorpe_media -R')
    sudo('chmod 777 /srv/calthorpe_media -R')


@task
def public_key():
    """
    prints out public ssh key to stdout
    """

    if not exists('~/.ssh/id_rsa.pub'):
        print 'Key does not exist. Generating new one...'
        run('ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa')

    print "\n\n Please make sure the following key is listed as a deployment key\n" \
          " in the repo if you want to be able to do setup_urbanfootprint\n\n"
    run('cat ~/.ssh/id_rsa.pub')


@task
def install_sproutcore():
    """
    get all Ruby rvm dependencies working alongside sproutcore
    we want to do a multiuser install of rvm (hence why we pipe to `sudo bash` instead of just `bash`)
    Also, we intentionally use the env.user (because he can sudo) and not env.deploy_user (that cannot sudo).
    :return:
    """
    # try:
    #     run('sproutcore')
    # except:
    try:
        sudo('apt-get remove --purge ruby-rvm ruby --yes')
        sudo('rm -rf /usr/share/ruby-rvm /etc/rmvrc /etc/profile.d/rvm.sh')
        sudo('apt-get install build-essential --yes')
        sudo('\curl -L https://get.rvm.io | bash -s stable --ruby --autolibs=3 --ruby=1.9.3')
        sudo('apt-get install -y build-essential openssl libreadline6 libreadline6-dev curl git-core zlib1g '
             'zlib1g-dev libssl-dev libyaml-dev libxml2-dev libxslt-dev autoconf libc6-dev ncurses-dev automake libtool '
             'bison subversion pkg-config sqlite3 libsqlite3-dev')
        sudo('curl -L https://get.rvm.io | bash -s stable --ruby') # modified to install just to the calthorpe user

        append('.bashrc', '''
        [[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" # This loads RVM into a shell session''',
               use_sudo=True)

        #for local setup: [[ -s "/usr/local/rvm/scripts/rvm" ]] && source "/usr/local/rvm/scripts/rvm" # This loads RVM into a shell session

        run('source /usr/local/rvm/scripts/rvm')

        sudo("rvm install ruby-1.9.3")
        sudo("rvm use 1.9.3")
        sudo("rvm --default use 1.9.3")
        sudo("gem install sproutcore")

        cuisine.group_user_ensure('rvm', env.user)
        cuisine.group_user_ensure('rvm', env.deploy_user)
    except Exception, E:
        print E


@task
def install_mapnik():
    """
    because mapnik requires some special steps to get set up, we do them before the rest of the package installations,
    so that we get it right the first time
    :return:
    """
    sudo("add-apt-repository ppa:mapnik/boost --yes")
    sudo("add-apt-repository ppa:mapnik/v2.2.0 --yes")
    sudo("apt-get update --yes")
    sudo("apt-get install libboost-dev libboost-filesystem-dev libboost-program-options-dev libboost-python-dev \
    libboost-regex-dev libboost-system-dev libboost-thread-dev --yes")
    sudo("apt-get build-dep python-imaging --yes")
    # create symlinks from the deps to a place where PIL will find them
    try:
        sudo("ln -f -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/")
        sudo("ln -f -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/")
        sudo("ln -f -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib")
    except:
        print "symlinks already created... passing"

    # make sure that osgeo is installed

    virtualenv("pip install PIL")
    sudo("apt-get install libmapnik mapnik-utils python-mapnik --yes")
    # Since we can't install mapnik in the virtualenv, soft link to the installation
    try:
        sudo('ln -f -s /usr/lib/pymodules/python2.7/mapnik/ {env}/lib/python2.7/site-packages/mapnik'.format(env=env.virtualenv_directory))
    except:
        print "link to mapnik installation already present"


@task
def install_osgeo():
    sudo('apt-get install python-gdal --yes')
    try:
        sudo('ln -f -s /usr/lib/python2.7/dist-packages/osgeo {env}/lib/python2.7/site-packages/'.format(env=env.virtualenv_directory))
    except:
        print "symlink to osgeo already created"


@task
def patch_django_layermapping():
    """
    the layermapping utility in django has a bug that prevents null foreign keys from getting imported
    properly. this patch, found at the bug documentation page https://code.djangoproject.com/ticket/17018
    is given a symbolic link to replace the standard django library file, which is renamed to layermapping.py.orig
    :return:
    """
    sudo('mv {env}/lib/python2.7/site-packages/django/contrib/gis/utils/layermapping.py '
         '{env}/lib/python2.7/site-packages/django/contrib/gis/utils/layermapping.py.orig'.format(env=env.virtualenv_directory))
    sudo('ln -s {PROJ_ROOT}/main/utils/layermapping.py '
         '{env}/lib/python2.7/site-packages/django/contrib/gis/utils/layermapping.py'.format(PROJ_ROOT=PROJ_PATH,
                                                                                             env=env.virtualenv_directory))


@task
def nginx_configure():
    """
    install nginx to proxy all calls in the development environment and static calls in production
    """

    sudo("apt-get install nginx --yes --ignore-missing")

    extension = 'dev' if env.dev else 'prod'

    with cd('/etc/nginx/sites-available'):
        sudo('rm -f default')
        sudo('rm -f calthorpe.nginx')
        sudo('ln -sf {SERVER_ROOT}/conf/etc/nginx/sites-available/calthorpe.nginx.{ext} calthorpe.nginx'.format(SERVER_ROOT=SERVER_ROOT, ext=extension))

        with cd('../sites-enabled'):
            sudo('rm -f default')
            sudo('rm -f calthorpe.nginx')
            sudo('ln -s ../sites-available/calthorpe.nginx .')

    sudo('/etc/init.d/nginx restart')


@task
def create_template_postgis():
    #with settings(warn_only=False):
    if not exists(POSTGIS_PATH):
        with cd("$HOME"):
            run("wget http://download.osgeo.org/postgis/source/postgis-1.5.8.tar.gz")
            run("tar xfvz postgis-1.5.8.tar.gz")
        with cd("$HOME/postgis-1.5.8"):
            run("./configure")
            run("make")
            sudo("make install")

        run_as_postgres('createdb -E UTF8 template_postgis')
        run_as_postgres('psql template_postgis -f {0}/postgis.sql'.format(POSTGIS_PATH))
        run_as_postgres('psql template_postgis -f {0}/spatial_ref_sys.sql'.format(POSTGIS_PATH))


def redis_install():
    sudo('apt-get install redis-server --yes')
    # Deal with Redis
    with cd('/etc/init.d/'):
        if not exists('/etc/init.d/redis', use_sudo=True, verbose=False):
            sudo('wget https://raw.github.com/ijonas/dotfiles/master/etc/init.d/redis-server')
        sudo('chmod +x /etc/init.d/redis-server')
    with cd('/etc/'):
        if not exists('/etc/redis.conf', use_sudo=True, verbose=False):
            sudo('wget https://raw.github.com/ijonas/dotfiles/master/etc/redis.conf')
        sudo('mkdir -p /var/lib/redis')
        with settings(warn_only=True):
            sudo('useradd --system --home-dir /var/lib/redis redis')
        sudo('chown redis.redis /var/lib/redis')
        sudo('update-rc.d redis-server defaults')

        #TODO:make  sure that $DAEMON matches the install path of redis-server (use: which redis-server to see
        # where it's installed)s

        with settings(warn_only=True):
            sed('redis-server', r'^DAEMON_ARGS=.*', 'DAEMON_ARGS=/etc/redis/redis.conf',
                backup='', use_sudo=True)
    sudo('/etc/init.d/redis-server restart')


def celery_install():
    #Set up Celery
    with cd('/etc/init.d/'):
        if not exists('/etc/init.d/celeryevcam', use_sudo=True, verbose=False):
            sudo('wget https://raw.github.com/ask/celery/master/contrib/generic-init.d/celeryevcam '
                 'https://raw.github.com/ask/celery/master/contrib/generic-init.d/celeryd ')
        sudo('chmod a+x celery*')
        sudo('ln -sf {SERVER_ROOT}/conf/celery/etc/default/celeryd /etc/default/celeryd'.format(SERVER_ROOT=SERVER_ROOT))
        sudo('ln -sf {SERVER_ROOT}/conf/celery/etc/default/celeryev /etc/default/celeryev'.format(SERVER_ROOT=SERVER_ROOT))
        sudo('touch /var/log/celeryev.log ')
        sudo('chown urbanfootprint:www-data /var/log/celeryev.log')


def setup_DB():
    sudo('add-apt-repository ppa:ubuntugis/ubuntugis-unstable --yes')
    sudo('apt-get install postgresql postgresql-9.1-postgis postgresql-contrib postgresql-server-dev-9.1 \
    postgresql-client postgresql-client-9.1 postgresql-client-common postgresql-contrib-9.1 postgresql-doc \
         postgresql-doc-9.1 --yes')
    with settings(warn_only=True):
        sudo('''createuser -sdr urbanfootprint''', user='postgres')
    with settings(warn_only=True):
        sed('/etc/postgresql/9.1/main/postgresl.conf',
            r"#.*listen_addresses='localhost'",
            "listen_addresses='*'",
            backup='', use_sudo=True)
    sudo('apt-get install libgeos-dev libgdal1-dev proj --yes')

    create_template_postgis()

    run('createdb urbanfootprint --template template_postgis')

    #Install dblink module
    run('psql urbanfootprint -c "CREATE EXTENSION dblink"')

    # TODO: edit or replace /etc/postgresql/9.1/main/postgresql.conf
    # this doesn't yet work from the command line...

    # TODO: why do we do this? --eb
    run('''psql urbanfootprint -c "alter user urbanfootprint password 'uf';" ''')

    sudo('/etc/init.d/postgresql restart')
    sudo('/etc/init.d/apache2 restart')


def install_postGIS2():
    sudo('apt-get install libgeos-dev')
    sudo('apt-get install libgdal1-dev')
    sudo('apt-get install proj')
    with cd('/tmp'):
        sudo('wget http://postgis.refractions.net/download/postgis-2.0.1.tar.gz')
        sudo('tar -xzf postgis-2.0.1.tar.gz')
    with cd('/tmp/postgis-2.0.1'):
        sudo('./configure --with-raster --with-topology')
        sudo('make')
        sudo('make comments')
        sudo('make install')
        sudo('make comments-install')
    run('psql urbanfootprint -c "create extension postgis";')
    run('psql urbanfootprint -c "create extension postgis_topology";')


def tilestache_configure():
    """Tilestache runs as an apache2 mod_wsgi process on port 8181
    (we are not currently running tilestache this way, rather, through our Django urls)
    """
    with cd('''/etc/apache2'''):
        try:
            sudo('ln -s {SERVER_ROOT}/conf/tilestache.apache /etc/apache2/sites-available'.format(SERVER_ROOT))
            sudo('ln -s {SERVER_ROOT}/conf/tilestache.apache /etc/apache2/sites-enabled'.format(SERVER_ROOT))
            sudo('rm -f /etc/apache2/sites-enabled/000-default')
        except:
            pass
        sed('/etc/apache2/ports.conf', r"NameVirtualHost *:80",
            "NameVirtualHost *:80\nNameVirtualHost *:8080", backup='', use_sudo=True)
        sed('/etc/apache2/ports.conf', r"Listen *:80", "Listen *:80\nListen *:8080",
            backup='', use_sudo=True)


@task
def install_filegdb(upgrade=True):
    with cd(TEMP_DIR):
        proj_filename = 'proj-%s.tar.gz' % PROJ_VER
        geos_filename = 'geos-%s.tar.bz2' % GEOS_VER

        run('wget -c %s' % (FILEGDBAPI_LOCATION,))
        run('wget -c http://download.osgeo.org/proj/%s' % (proj_filename,))
        run('wget -c http://download.osgeo.org/geos/%s' % (geos_filename,))

        run('tar xzf %s' % (FILEGDBAPI_FILE,))
        run('tar xzf %s' % (proj_filename,))
        run('tar xjf %s' % (geos_filename,))

        #install FILEGDB API based on current ESRI defaults
        sudo('rm -rf /usr/local/FileGDB_API 2>/dev/null')
        sudo('mv FileGDB_API /usr/local/FileGDB_API')
        #sudo('echo \"/usr/local/FileGDB_API/lib\"  > /etc/ld.so.conf.d/filegdb.conf')

        with settings(warn_only=True):
            sudo('ln -s /usr/local/FileGDB_API/lib/* /usr/local/lib/')
     # For SH and variants (sh, bash, etc...):
            #fix start
            sudo('ln -s /usr/local/lib/libfgdbunixrtl.so /usr/local/lib/libfgdblinuxrtl.so')
     #     export LD_LIBRARY_PATH

        sudo('ldconfig')

        with cd('proj-%s' % PROJ_VER):
            run('./configure')
            if upgrade:
                run('make clean')
            run('make')
            sudo('make install')
            sudo('ldconfig')

        with cd('geos-%s' % GEOS_VER):
            run('./configure')
            if upgrade:
                run('make clean')
            run('make')
            sudo('make install')
            sudo('ldconfig')

# @task
# def install_gdal(upgrade=True):

     # For SH and variants (sh, bash, etc...):
     #     LD_LIBRARY_PATH=<your location>/FileGDB_API/lib:$LD_LIBRARY_PATH
     #     export LD_LIBRARY_PATH
    sudo('ln -sf /usr/local/lib/libfgdbunixrtl.so /usr/local/lib/libfgdblinuxrtl.so')

    with cd(TEMP_DIR):
        gdal_filename = 'gdal-%s.tar.gz' % GDAL_VER
        run('wget -c http://download.osgeo.org/gdal/%s/%s' % (GDAL_VER, gdal_filename,))

        run('tar xzf %s' % (gdal_filename,))
        sudo('ln -sf /usr/local/FileGDB_API/lib/* /usr/local/lib/')
        with cd('gdal-%s' % GDAL_VER):
            with shell_env(LD_LIBARY_PATH='/usr/local/FileGDB_API/lib'):
                sudo('ldconfig')
                run('./configure --with-python --with-fgdb=/usr/local/FileGDB_API')
                if upgrade:
                    run('make clean')
                run('make')
                sudo('make install')
                sudo('ldconfig')


@task
def setup_personal_dev_environment():
    """
    takes a default VM setup and configures it to a particular user
    """

    user_name = prompt("please enter your git username (as appears in the VCS): ")
    email = prompt("please enter your email address: ")
    vm_name = prompt("please enter a new name for this VM: ")

    sudo('su {0} -c "git config --global user.email \'{1}\'"'.format(env.user, email))
    sudo('su {0} -c "git config --global user.name \'{1}\'"'.format(env.user, user_name))

    sudo('hostname \'{0}\''.format(vm_name))

    sed('/etc/hosts', "defaultVM", vm_name, use_sudo=True)

    sed('/etc/hostname', 'defaultVM', vm_name, use_sudo=True)


