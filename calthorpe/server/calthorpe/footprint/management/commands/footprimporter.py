# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
# 
# Copyright (C) 2012 Calthorpe Associates
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
from optparse import make_option
from django.core.management.base import BaseCommand
from footprint.database.import_data import ImportData

class Command(BaseCommand):
    """
        The Footprint importer (footprimporter) is used to synchronize a local system to the data of remote source. There are two import situations. The first is importing from "raw" database tables that are formatted for the UrbanFootprint beta (0.*). This is the beta schema which uses input_outputs_STUDY_AREA where the study area is the old representation of project. The second import situation is to import from a UrbanFootprint 1.* database, where the source schemas match the structure of the new. Use the -v option and specify 0 for the beta schema and 1 for the 1.* version. The default is the beta for now.
    """
    option_list = BaseCommand.option_list + (
        make_option('--db', help='A database settings key. Use this instead of host, port, user, password, and database'),
        make_option('--host', default='localhost', help='The source database host name'),
        make_option('-P', '--port', default='', help='The source database port'),
        make_option('-U', '--user',  help='The source database user name'),
        make_option('-p', '--password', help='The source database password'),
        make_option('-d', '--database', help='The source database name'),
        make_option('--config_entity', help='The ConfigEntity key of the ConfigEntity whose feature tables are to be imported'),
        make_option('--db_entity_key', help='The db_entity_key for which to import feature tables. If not specified all DbEntities that map to a Feature class will import their table'),
        make_option('--test', action='store_true', default=False, help='If set only a portion of the geographic data is copied from the Feature table to save time and space. Default all is copied. If the code will first look for a version of the Feature table with "_sample" appended. It will import this if found and otherwise a portion of the full table will be cropped'),
        make_option('--dump_only', action='store_true', default=False, help='If set only table dumps can occur, not selecting rows from the source database tables using db_link. This is useful when the source database is not accessible by the target from within a psql call. This should only be used on an empty target database. Not compatible with --test.')
    )

    def handle(self, *args, **options):
        import_data = ImportData(**options)
        self.stdout.write("pg_dump connection string: {0}\n".format(import_data.pg_dump_connection))
        self.stdout.write("db_link connection string: {0}\n".format(import_data.db_link_connection))
        self.stdout.write("target database connection string: {0}\n".format(import_data.target_database_connection))
        import_data.run()
