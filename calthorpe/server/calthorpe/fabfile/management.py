import os
import sys
import shutil
from cuisine_postgresql import postgresql_role_ensure, postgresql_database_ensure, postgresql_database_check, run_as_postgres
from fabric.context_managers import cd, settings
from fabric.contrib.console import confirm
from fabric.decorators import task
from fabric.operations import sudo, local
from fabric.state import env
from fabfile.installation import PROJ_ROOT, SERVER_ROOT, manage_py, virtualenv, setup_databases, set_paths

__author__ = 'calthorpe'


from fabric.contrib import django

django.settings_module('calthorpe.settings')

from django.conf import settings as django_settings


@task
def test_sproutcore_nobuild():
    with cd('/etc/nginx/sites-available'):
        sudo('rm -f default')
        sudo('rm -f calthorpe.nginx')
        sudo('ln -s {SERVER_ROOT}/conf/etc/nginx/sites-available/calthorpe.nginx.dev calthorpe.nginx'.format(SERVER_ROOT=SERVER_ROOT))
        sudo('service nginx restart')


@task
def test_sproutcore_build(upgrade_env=True):
    build_sproutcore(upgrade_env)

    # sets nginx configuration to point to the scbuild configuration

    with cd('/etc/nginx/sites-available'):
        sudo('rm -f default')
        sudo('rm -f calthorpe.nginx')
        sudo('ln -s {SERVER_ROOT}/conf/etc/nginx/sites-available/calthorpe.nginx.dev.scbuild calthorpe.nginx'.format(SERVER_ROOT=SERVER_ROOT))
        sudo('service nginx restart')


def drop_databases():
    """
        Drop the databases. This is not part of the normal setup process, rather it's used to recreate the database in development.
    :return:
    """

    sudo('service postgresql restart')
    for database_name in ['test_urbanfootprint', 'urbanfootprint']:
        if postgresql_database_check(database_name):
            # Drop the database if it exists
            cmd = 'dropdb -U postgres {database_name}'.format(
                database_name=database_name,
            )
            run_as_postgres(cmd)


@task
def switch_to_prod(reverse=False):
    extension = 'dev' if reverse else 'prod'
    try:
        sudo('rm /etc/supervisor/conf.d/calthorpe.conf')
        sudo('rm /etc/nginx/sites-available/calthorpe.nginx')
    except:
        pass

    sudo('ln -sf {server_root}/conf/etc/nginx/sites-available/calthorpe.nginx.{nginx} '
         '/etc/nginx/sites-available/calthorpe.nginx '.format(server_root=SERVER_ROOT, nginx=extension))
    sudo('ln -sf {server_root}/conf/etc/supervisor/conf.d/calthorpe.supervisor.{extension} '
         '/etc/supervisor/conf.d/calthorpe.conf'.format(server_root=SERVER_ROOT, extension=extension))
    sudo('service nginx reload')
    sudo('service nginx restart')
    sudo('supervisorctl stop all')
    sudo('supervisorctl reload')
    sudo('supervisorctl start all')


@task
def update_published_data():
    manage_py('footprint_init --skip --results --tilestache')


@task
def recreate_django():
    """
        Like recreate_dev but leaves the data tables in place while wiping out all the Django tables
        Make sure complete migration scripts exist prior to running this
    :return:
    """
    if '127.0.0.1' not in env.hosts and not getattr(env, 'allow_remote_recreate', False):
        raise Exception("recreate_dev is not allowed for non-localhosts for security purposes")

    sudo('service postgresql restart')

    manage_py('footprint_init --skip --destroy_layer_selection_tables')

    database_name = 'urbanfootprint'
    cmd = 'pg_dump -U postgres -Fc {database_name} -n public > /tmp/footprint_public.dump'.format(
        database_name=database_name,
    )
    run_as_postgres(cmd)

    cmd = 'pg_dump -U postgres -Fc {database_name} -N public > /tmp/footprint_schemas.dump'.format(
        database_name=database_name,
    )
    run_as_postgres(cmd)

    cmd = 'dropdb -U postgres {database_name}'.format(
        database_name=database_name,
    )
    run_as_postgres(cmd)

    postgresql_role_ensure('calthorpe', 'Calthorpe123', superuser=True, createdb=True, createrole=True,
                           inherit=True, login=True)
    postgresql_database_ensure('urbanfootprint', owner='calthorpe', template='template_postgis')

    with cd(PROJ_ROOT):
        manage_py('syncdb --noinput')
        manage_py('migrate')

    for public_import_table in map(
            lambda name: 'footprint_%s' % name,
            ['geography', 'medium', 'template', 'buildingattributes', 'buildingattributeset', 'builtform', 'placetype', 'placetypecomponentcategory', 'placetypecomponent', 'primarycomponent', 'sacoglandusedefinition', 'sacoglanduse', 'scaglandusedefinition', 'scaglanduse', 'sacramento*']):
        cmd = 'pg_restore -U postgres -d {database_name} --data-only -t {public_import_table} /tmp/footprint_public.dump'.format(
            database_name=database_name,
            public_import_table=public_import_table
        )
        run_as_postgres(cmd)

    cmd = 'pg_restore -U postgres -d {database_name} /tmp/footprint_schemas.dump'.format(
        database_name=database_name,
    )
    run_as_postgres(cmd)

    python = os.path.join(env.virtualenv_directory, 'bin/python')
    output = local(python + ' ' + PROJ_ROOT + '/manage.py sqlsequencereset footprint', capture=True).replace('BEGIN;\n','').replace('COMMIT;','')

    with settings(warn_only=True):
        cmd = 'psql -U postgres -d {database_name} -c "{output}"'.format(
           database_name=database_name,
           output=output
        )
        run_as_postgres(cmd)
    with cd(PROJ_ROOT):
        manage_py('collectstatic --noinput')
        manage_py('footprint_init')

    if os.path.exists('/tmp/stache'):
        shutil.rmtree('/tmp/stache')


@task
def recreate_dev():
    """
        Drops and recreates the databases for development, then initializes footprint
        This will raise an error if 127.0.0.1 is not in env.hosts to protect live databases
        Make sure complete migration scripts exist prior to running this
    :return:
    """

    if '127.0.0.1' not in env.hosts and not getattr(env, 'allow_remote_recreate', False):
        raise Exception("recreate_dev is not allowed for non-localhosts for security purposes")
    if not getattr(env, 'allow_remote_recreate', False):
        if not confirm("This command destroys the database and regenerates it -- proceed?", default=False):
            return
        if not django_settings.USE_SAMPLE_DATA_SETS:
            if not confirm("THIS IS A PRODUCTION DATA SET! REALLY DELETE IT?", default=False):
                return

    drop_databases()
    setup_databases()

    with cd(PROJ_ROOT):
        manage_py('syncdb --noinput')
        manage_py('migrate')
        manage_py('collectstatic --noinput')
        manage_py('footprint_init')

    if os.path.exists('/tmp/stache'):
        shutil.rmtree('/tmp/stache')


@task
def build_sproutcore(upgrade_env=True):
    with cd(PROJ_ROOT):
        # build sproutcore
        with cd('./footprint/sproutcore'):
            sudo('rm -rf builds')
            # Build footprint in the build dir
            sudo('sproutcore build fp --buildroot=builds --dont_minify', user=env.deploy_user)
            # Change ownership on output
            sudo('chown -R {0}.www-data ./builds'.format(env.deploy_user))

        with cd('./footprint/static'):
            # ln to the builds dir from Django's static dir
            sudo('ln -f -s ../sproutcore/builds/static/* .', user=env.deploy_user)

        with cd('./footprint/templates/footprint'):
            # ln to the fp index.html
            sudo('ln -f -s ../../sproutcore/builds/static/fp/en/0.1/index.html .', user=env.deploy_user)

        # do a collect static to grab all static files and link them to the right directory
        manage_py('collectstatic -l --noinput')

        # we intentionally stop and then start (instead of restart)


@task
def deploy(upgrade_env=True):
    '''
    Deploy code, pip dependencies and execute migrations
    '''

    set_paths()

    with cd(PROJ_ROOT):
        sudo('git pull', user=env.deploy_user)

        #with cd('/srv/calthorpe/urbanfootprint'):
        #with settings(warn_only=True):
        #    sudo('su {0} -c "git rm -r --cached ."'.format(env.deploy_user))
        #    sudo('su {0} -c "rm -rf /srv/calthorpe/urbanfootprint/calthorpe/server/calthorpe/footprint/sproutcore/frameworks/sc-table"'.format(env.deploy_user))
        #    sudo('su {0} -c "git submodule add https://github.com/jslewis/sctable.git /srv/calthorpe/urbanfootprint/calthorpe/server/calthorpe/footprint/sproutcore/frameworks/sc-table"'.format(env.deploy_user))
        #sudo('su {0} -c "git submodule init"'.format(env.deploy_user))
        #sudo('su {0} -c "git submodule update"'.format(env.deploy_user))

        if (upgrade_env == True):
            virtualenv('pip install -U -r ' + PROJ_ROOT + '/pip-req.txt')
        else:
            virtualenv('pip install -r ' + PROJ_ROOT + '/pip-req.txt')

        manage_py('syncdb --noinput')

        # just adding the --delete-ghost-migrations flag until everything runs
        manage_py('migrate --delete-ghost-migrations')

        #        manage_py('footprint_init')

        build_sproutcore(upgrade_env)
        # because of a bug the very first time it is ran where the restart
    # won't load the new configuration files

    with settings(warn_only=True):
        sudo('supervisorctl stop all')
        sudo('/etc/init.d/supervisor stop')
        sudo('/etc/init.d/nginx stop')
        # sudo('/etc/init.d/varnish stop')

    sudo('/etc/init.d/supervisor start')
    sudo('supervisorctl start all')
    sudo('/etc/init.d/nginx start')
    # sudo('/etc/init.d/varnish start')


@task
def basic_deploy():
    deploy(upgrade_env=False)