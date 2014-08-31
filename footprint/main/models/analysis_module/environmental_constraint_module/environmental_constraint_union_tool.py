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
import logging
import time
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.analysis_module.analysis_tool import AnalysisTool
from footprint.main.models.geospatial.behavior import BehaviorKey
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey
from footprint.main.utils.uf_toolbox import drop_table, execute_sql, add_geom_idx, create_sql_calculations
from footprint.main.utils.utils import parse_schema_and_table

logger = logging.getLogger(__name__)

__author__ = 'calthorpe'


class EnvironmentalConstraintUnionTool(AnalysisTool):

    objects = GeoInheritanceManager()

    class Meta(object):
        app_label = 'main'
        abstract = False

    def initialize(self, created):
        self.update()

    def update(self):
        """
            This function handles the update or creation on the environmental constraints geography producing the area
            for each layer with the environmental constraint behavior. This function will both add and remove
            constraints and produce the final constraints layer in the primary geography of the active scenario
        """

        start_time = time.time()

        current_db_entities = \
            set(self.config_entity.db_entities_having_behavior_key(BehaviorKey.Fab.ricate('environmental_constraint')))

        base_feature_class = self.config_entity.db_entity_feature_class(
            DbEntityKey.BASE)

        options = dict(
            project_schema=parse_schema_and_table(base_feature_class._meta.db_table)[0],
            base_table=base_feature_class.db_entity_key
        )

        logger.info('Inserting raw geographies into the environmental constraint geographies table for DbEntities: %s' % \
                    ', '.join(map(lambda db_entity: db_entity.name, current_db_entities)))

        drop_table('{project_schema}.environmental_constraint_geographies_table'.format(
            project_schema=options['project_schema'])
        )

        current_environmental_constraints = []
        for db_entity in current_db_entities:
            constraint_class = self.config_entity.db_entity_feature_class(db_entity.key)
            current_environmental_constraints.append(constraint_class.db_entity_key)

        create_id_field_format = create_sql_calculations(current_environmental_constraints, ', {0}_id int')
        insert_id_field_format = create_sql_calculations(current_environmental_constraints, ', {0}_id')

        pSql = '''
        create table {project_schema}.environmental_constraint_geographies_table
            (primary_id integer, wkb_geometry geometry {create_id_field_format});
        '''.format(project_schema=options['project_schema'], create_id_field_format=create_id_field_format)

        execute_sql(pSql)

        for db_entity in current_db_entities:
            logger.info('Inserting into environmental constraint geographies table for DbEntity: %s' % db_entity.full_name)

            constraint_class = self.config_entity.db_entity_feature_class(db_entity.key)

            pSql = '''
                insert into {project_schema}.environmental_constraint_geographies_table (primary_id, wkb_geometry, {constraint_db_entity_key}_id) select
                    cast(primary_id as int), wkb_geometry, {constraint_db_entity_key}_id from (
                    select
                        geography_id as primary_id,
                        {constraint_db_entity_id} as {constraint_db_entity_key}_id,
                        st_setSRID(st_transform(st_buffer((st_dump(wkb_geometry)).geom, 0), 3310), 3310) as wkb_geometry

                    from (
                        select b.geography_id, st_intersection(a.wkb_geometry, b.wkb_geometry) as wkb_geometry
	                    from {constraint_schema}.{constraint_db_entity_key} a,
                        {project_schema}.{base_table} b
                            where st_intersects(a.wkb_geometry, b.wkb_geometry)) as intersection
                    ) as polygons;
                '''.format(
                project_schema=options['project_schema'],
                base_table=options['base_table'],
                constraint_schema=parse_schema_and_table(constraint_class._meta.db_table)[0],
                constraint_db_entity_key=constraint_class.db_entity_key,
                constraint_db_entity_id=db_entity.id
            )

            execute_sql(pSql)

            logger.info('finished inserting db_entity: {db_entity} {time} elapsed'.format(
                time=time.time() - start_time,
                db_entity=constraint_class.db_entity_key))

        #only regenerate the merged environmental constraint whenever an envrionmental constraint is added or removed
        # from the layer

        add_geom_idx(options['project_schema'], 'environmental_constraint_geographies_table')

        logger.info('Unioning all environmental constraint geographies')
        drop_table('{project_schema}.environmental_constraint_geographies_table_unioned'.format(
            project_schema=options['project_schema'])
        )

        pSql = '''
            CREATE TABLE {project_schema}.environmental_constraint_geographies_table_unioned
                (id serial, wkb_geometry geometry, acres float, primary_id int {create_id_field_format});
        '''.format(project_schema=options['project_schema'], create_id_field_format=create_id_field_format)

        execute_sql(pSql)

        pSql = '''
        insert into {project_schema}.environmental_constraint_geographies_table_unioned (wkb_geometry, acres, primary_id {insert_id_field_format})
               SELECT
                    st_buffer(wkb_geometry, 0) as wkb_geometry,
                    st_area(st_buffer(wkb_geometry, 0)) * 0.000247105 as acres,
                    primary_id {insert_id_field_format}

                    FROM (
                        SELECT
                            (ST_Dump(wkb_geometry)).geom as wkb_geometry,
                            primary_id {insert_id_field_format}

                        FROM (
                            SELECT ST_Polygonize(wkb_geometry) AS wkb_geometry, primary_id {insert_id_field_format}   FROM (
                                SELECT ST_Collect(wkb_geometry) AS wkb_geometry, primary_id {insert_id_field_format}   FROM (
                                    SELECT ST_ExteriorRing(wkb_geometry) AS wkb_geometry, primary_id {insert_id_field_format}
                                        FROM {project_schema}.environmental_constraint_geographies_table) AS lines
                                            group by primary_id {insert_id_field_format}) AS noded_lines
                                                group by primary_id {insert_id_field_format}) as polygons
                    ) as final
                WHERE st_area(st_buffer(wkb_geometry, 0)) > 5;'''.format(
            project_schema=options['project_schema'],
            insert_id_field_format=insert_id_field_format
        )

        execute_sql(pSql)

        logger.info('finished unioning env constraints: {time} elapsed'.format(
            time=time.time() - start_time))

        #reproject table back to 4326 for integration with web viewing
        pSql = '''
        update {project_schema}.environmental_constraint_geographies_table_unioned a set wkb_geometry = st_transform(st_buffer(wkb_geometry, 0), 4326)
        '''.format(
            project_schema=options['project_schema']
        )
        execute_sql(pSql)

        add_geom_idx(options['project_schema'], 'environmental_constraint_geographies_table_unioned')

        logger.info('Env Union Finished: %s' % str(time.time() - start_time))
