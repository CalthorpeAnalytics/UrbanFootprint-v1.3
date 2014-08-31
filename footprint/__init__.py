import logging
import os
from fabric.operations import sudo
from fabric.state import env
logger = logging.getLogger(__name__)

# if not os.environ.get('IS_CELERY', None):
#     logger.info('restarting celery')
#     env.host_string = 'localhost'
#     env.user = 'calthorpe'
#     env.sudo_user = 'calthorpe'
#     env.password = '[ your password ]'
#     sudo('supervisorctl restart celery_worker', tty=False)