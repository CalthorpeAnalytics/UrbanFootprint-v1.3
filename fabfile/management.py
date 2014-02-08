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


import fileinput
import glob
import os
import re
import sys
import shutil
from cuisine_postgresql import postgresql_role_ensure, postgresql_database_ensure, postgresql_database_check, run_as_postgres
import datetime
from fabric.context_managers import cd, settings
from fabric.contrib.console import confirm
from fabric.decorators import task
from fabric.operations import sudo, local, run
from fabric.state import env
from fabfile.installation import PROJ_ROOT, SERVER_ROOT, manage_py, virtualenv, setup_databases, set_paths, directory_permissions
import logging
logger = logging.getLogger(__name__)
__author__ = 'calthorpe_associates'


from fabric.contrib import django

django.settings_module('footprint.settings')

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
         ' /etc/supervisor/conf.d/calthorpe.conf'.format(server_root=SERVER_ROOT, extension=extension))
    sudo('service nginx reload')
    sudo('service nginx restart')
    sudo('supervisorctl stop all')
    sudo('supervisorctl reload')
    sudo('supervisorctl start all')


@task
def restart_celery():
    sudo('supervisorctl restart celery_worker')
    sudo('supervisorctl restart celerybeat')


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

    manage_py('footprint_init --skip --relayer_selection')

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

    postgresql_role_ensure('calthorpe', '[PASSWORD]', superuser=True, createdb=True, createrole=True,
                           inherit=True, login=True)
    postgresql_database_ensure('urbanfootprint', owner='calthorpe', template='template_postgis')

    with cd(PROJ_ROOT):
        manage_py('syncdb --noinput')
        manage_py('migrate')

    for public_import_table in map(
            lambda name: 'main_%s' % name,
            ['geography', 'medium', 'template', 'buildingattributes', 'buildingattributeset', 'builtform', 'placetype',
             'placetypecomponentcategory', 'placetypecomponent', 'primarycomponent', 'sacoglandusedefinition', 'sacoglanduse', 'scaglandusedefinition', 'scaglanduse', 'sutter*']):
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
    output = local(python + ' ' + PROJ_ROOT + '/manage.py sqlsequencereset main', capture=True).replace('BEGIN;\n','').replace('COMMIT;','')

    with settings(warn_only=True):
        cmd = 'psql -U postgres -d {database_name} -c "{output}"'.format(
           database_name=database_name,
           output=output
        )
        run_as_postgres(cmd)
    with cd(PROJ_ROOT):
        manage_py('collectstatic --noinput')
        manage_py('footprint_init')

    clear_tilestache_cache()


@task
def recreate_dev(init=True):
    """
        Drops and recreates the databases for development, then initializes main
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
        sudo('find . -name \'*.pyc\' -delete')
        manage_py('syncdb --noinput')
        manage_py('migrate')
        manage_py('collectstatic --noinput')

        if init is True:
            manage_py('footprint_init')

    clear_tilestache_cache()


@task
def clear_tilestache_cache():
    sudo('rm -rf /tmp/stache/*')
    sudo('chown -R calthorpe:www-data /tmp/stache')
    sudo('chmod -R ug+w /tmp/stache')


@task
def delete_all_cartocss():
    sudo("rm -r /srv/calthorpe_media/cartocss/*")
    sudo("rm -r /srv/calthorpe_static/cartocss/*")


@task
def build_sproutcore(upgrade_env=True):
    with cd(SERVER_ROOT):
        sudo('/srv/calthorpe_env/bin/fab localhost update_sproutcore_build_number')

    # build sproutcore
    with cd('{root}/sproutcore'.format(root=SERVER_ROOT)):
        sudo('rm -rf builds')
        # Build main in the build dir
        sudo('sproutcore build fp --buildroot=builds --dont_minify', user=env.deploy_user)
        # Change ownership on output
        sudo('chown -R {0}.www-data ./builds'.format(env.deploy_user))

        # ln to the builds dir from Django's static dir
    sudo('ln -f -s {root}/sproutcore/builds/static/* {root}/footprint/main/static'.format(root=SERVER_ROOT), user=env.deploy_user)

    sudo('ln -f -s {root}/sproutcore/builds/static/fp/en/0.1/index.html '
         '{root}/footprint/main/templates/footprint/index.html'.format(root=SERVER_ROOT), user=env.deploy_user)

    # do a collect static to grab all static files and link them to the right directory
    manage_py('collectstatic -l --noinput')

@task
def deploy(upgrade_env=True):
    """
    Deploy code, pip dependencies and execute migrations
    """

    set_paths()
    directory_permissions()
    with cd(PROJ_ROOT):
        sudo('find . -name \'*.pyc\' -delete')
        sudo('git pull', user=env.deploy_user)

        #with cd('/srv/calthorpe/urbanfootprint'):
        #with settings(warn_only=True):
        #    sudo('su {0} -c "git rm -r --cached ."'.format(env.deploy_user))
        #    sudo('su {0} -c "rm -rf /srv/calthorpe/urbanfootprint/calthorpe/server/calthorpe/main/sproutcore/frameworks/sc-table"'.format(env.deploy_user))
        #    sudo('su {0} -c "git submodule add https://github.com/jslewis/sctable.git /srv/calthorpe/urbanfootprint/calthorpe/server/calthorpe/main/sproutcore/frameworks/sc-table"'.format(env.deploy_user))
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
def update_license():
    def pre_append(line, file_name):
        fobj = fileinput.FileInput(file_name, inplace=1)
        first_line = fobj.readline()
        sys.stdout.write("%s\n%s" % (line, first_line))
        for line in fobj:
            sys.stdout.write("%s" % line)
        fobj.close()

    boilerplate_file = open('/footprint/LICENSE', 'r')
    boilerplate = boilerplate_file.read()
    boilerplate_file.close()

    def sub_py(boilerplate):
        text = re.sub(r'^', '# ', boilerplate, 0, re.M)
        return re.sub(r'$', '\n', text, 1)
    def sub_js(boilerplate):
        text = re.sub(r'^', '* ', boilerplate, 0, re.M)
        text = re.sub(r'^', '/* \n', text, 1)
        return re.sub(r'$', '\n */\n', text, 1)
    def sub_html(boilerplate):
        text = re.sub(r'^', '<!-- \n', boilerplate, 1)
        return re.sub(r'$', '\n -->\n', text, 1)

    format_dict = {
        'py': sub_py(boilerplate),
        'js': sub_js(boilerplate),
        'css': sub_js(boilerplate),
        'html': sub_html(boilerplate)
    }

    files_to_check = collect_file_paths(django_settings.ROOT_PATH, ['py', 'js', 'css', 'html'])

    # remove old license text
    for path in files_to_check:
        old_license = re.compile(r"\sUrbanFootprint-California.*Web:\swww\.footprint\.com", re.S | re.M)
        o = open(path)
        data = o.read()
        o.close()
        if 'manage.py' in path:
            continue
        new_file_contents = re.sub(old_license, "", data)
        if new_file_contents:
            file = open(path, 'w')
            file.write(new_file_contents)
            file.close()

        ext = re.match(r'.*\.(\w+)$', path).group(1)

        if format_dict.get(ext):
            print path
            pre_append(format_dict[ext], path)


def collect_file_paths(root_path, extensions):
    files_to_check = []
    for r, d, f in os.walk(root_path):
        for ext in extensions:
            files_to_check.extend(glob.glob(os.path.join(r, "*.{0}".format(ext))))
    return files_to_check

@task
def update_sproutcore_build_number():
    print 'updating sc build on ' + str(env.hosts)
    build_number_format = "{year}.{month}.{day}".format

    today = datetime.date.today()

    build_number = build_number_format(year=today.year, month=today.month, day=today.day)
    print build_number

    sproutcore_directory = os.path.join(django_settings.SERVER_ROOT, 'sproutcore')

    files_to_inspect = collect_file_paths(sproutcore_directory, ['js'])

    old_revision_line = re.compile(r"value:\s'UrbanFootprint\srev\.\s\d{4}\.\d{1,2}\.\d{1,2}\s")

    updated = False
    for path in files_to_inspect:
        o = open(path)
        data = o.read()
        o.close()

        file_has_build_number = re.search(old_revision_line, data)
        if file_has_build_number:
            new_file_contents = re.sub(old_revision_line, "value: \'UrbanFootprint rev. {0} ".format(build_number), data)
            print "value: \'UrbanFootprint rev. {0} ".format(build_number)
            file = open(path, 'w')
            file.write(new_file_contents)
            file.close()
            print 'Updated build number in ' + path
            updated = True
    if not updated:
        print 'did not update build number!'