from contextlib import contextmanager
import os

def build_postgres_conn_string(db_settings, omit_db=False):
    '''
    Builds a postgres connection string based on the settings
    of a particular database (e.g settings.DATABASES['default'])
    '''

    # We may want to ommit port & host depending on how pg_hba.conf has been configured
    # (TCP sockets vs unix sockets). Specifying the port/host triggers a different authentication mechanism

    pg_conn_string = ''

    if len(db_settings['PORT']) > 0:
        pg_conn_string += '-p {port} '.format(port=db_settings['PORT'])

    if len(db_settings['HOST']) > 0:
        pg_conn_string += '-h {host} '.format(host=db_settings['HOST'])

    if len(db_settings['USER']) > 0:
        pg_conn_string += '-U {user} '.format(user=db_settings['USER'])

    if not omit_db:
        pg_conn_string += '{dbname}'.format(dbname=db_settings['NAME'])

    return pg_conn_string


@contextmanager
def postgres_env_password_loaded(db_settings):
    '''
    Sets postgres environment password to environment variable
    upon entry and unsets it on exit if it did not exist
    '''
    var_existed = False

    if 'PGPASSWORD' in os.environ:
        old_val = os.environ['PGPASSWORD']
        var_existed = True

    os.environ["PGPASSWORD"] = db_settings['PASSWORD']

    try:
        yield
    finally:
        if var_existed:
            os.environ['PGPASSWORD'] = old_val
        else:
            del os.environ['PGPASSWORD']
