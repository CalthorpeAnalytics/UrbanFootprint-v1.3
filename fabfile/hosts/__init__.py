from footprint.settings import CALTHORPE_DATA_DUMP_LOCATION

__author__ = 'calthorpe_associates'

from fabric.api import task, env

@task
def localhost(skip_ssh=False):
    """
    Sets up environment to pretend that localhost is a remote server
    """
    if not skip_ssh:
        env.hosts = ['127.0.0.1']

    env.user = env.deploy_user = 'calthorpe'
    env.deploy_user = 'calthorpe'
    env.virtualenv_directory = '/srv/calthorpe_env'
    env.password = '[ your password ]'
    env.DATA_DUMP_PATH = CALTHORPE_DATA_DUMP_LOCATION
    env.dev = True

# Add remote servers here
