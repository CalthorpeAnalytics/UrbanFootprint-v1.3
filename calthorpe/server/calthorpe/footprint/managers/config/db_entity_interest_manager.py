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
from footprint.lib.functions import unique
from footprint.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.models.config.interest import Interest
from footprint.models.geospatial.db_entity import DbEntity
from footprint.models.database.information_schema import InformationSchema
from footprint.models.keys.keys import Keys

__author__ = 'calthorpe'

class DbEntityInterestManager(GeoInheritanceManager):

    def sync_db_table_entities(self, config_entity):
        """
            Syncs the db_entities representing tables with the tables in the this instance's schema. This should only
            be used when tables are added or removed from the system outside of the UrbanFootprint application.
            Normally the db_entries will stay synced automatically. No DbEntry instances representing queries, views,
            or other table-based representations are added or deleted here.
        """
        # Load the db_entities that represent tables
        table_entities = config_entity.db_entities.filter(table__isnull=False, query__isnull=True)
        table_entity_names = map(lambda table_entity: table_entity.table, table_entities)
        # Load the physical tables in the schema
        table_names = unique(
            map(
                lambda information_schema: information_schema.table_name,
                InformationSchema.objects.filter(table_schema=config_entity.schema())))
        # Compare table names to find new tables for which to create entries
        owner_interest = Interest.objects.get(key=Keys.INTEREST_OWNER)
        for new_table_name in set(table_names) - set(table_entity_names):
            # Create the DbEntity and join it to the ConfigEntity with an owner DbEntityInterest
            table_entity = DbEntity.objects.create(name=new_table_name, schema=config_entity.schema(), table=new_table_name)
            self.create(config_entity=config_entity, db_entity=table_entity, interest=owner_interest)

        # Compare table names to find deleted tables for which to delete entries
        for table_entity in table_entities:
            if not table_entity.table in table_names:
                table_entity.delete()

