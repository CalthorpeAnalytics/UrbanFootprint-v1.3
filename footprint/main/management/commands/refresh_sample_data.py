from django.conf import settings
from django.core.management import BaseCommand
from sarge import run
from footprint.client.configuration.fixture import ConfigEntityFixture
from footprint.main.database.import_data import ImportData
from footprint.main.models import ConfigEntity, Region, Scenario, Project
from footprint.main.utils.utils import postgres_url_to_connection_dict
import psycopg2

__author__ = 'calthorpe'


class Command(BaseCommand):
    """
        This command connects to the source of the sample data and populates a local db
    """
    def drop_db(self):

        # Try to connect
        try:
            conn = psycopg2.connect("dbname='urbanfootprint' user='calthorpe' password='Calthorpe'")
        except Exception, E:
            raise E

        cur = conn.cursor()
        conn.set_isolation_level(0)
        try:
            cur.execute("""DROP DATABASE sample_data""")
            cur.execute("""CREATE DATABASE sample_data TEMPLATE template_postgis""")
        except Exception, E:
            raise E

    def handle(self, *args, **options):
        self.drop_db()
        project = Project.objects.all()[0]
        client_fixture = ConfigEntityFixture.resolve_config_entity_fixture(project)
        default_db_entity_configurations = client_fixture.default_db_entity_configurations()
        for db_entity_config in default_db_entity_configurations:
            importer = ImportData(config_entity=project, db_entity=db_entity_config)
            importer.target_database = settings.DATABASES['sample_data']
            importer.create_target_db_string()

            # For now we only import data for DbEntity instances with a configured database url
            connection_dict = postgres_url_to_connection_dict(db_entity_config['url'])
            # The import database currently stores tables as public.[config_entity.key]_[feature_class._meta.db_table (with schema removed)][_sample (for samples)]
            # We always use the table name without the word sample for the target table name
            source_table = "{0}_{1}_{2}".format(project.key, db_entity_config['table'], 'sample')
            importer._dump_tables_to_target('-t %s' % source_table,
                                            source_schema='public',
                                            target_schema='public',
                                            source_table=source_table,
                                            target_table=source_table,
                                            connection_dict=connection_dict)
