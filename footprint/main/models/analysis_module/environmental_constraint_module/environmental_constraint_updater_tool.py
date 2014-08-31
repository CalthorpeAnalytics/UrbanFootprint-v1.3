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

from django.contrib.gis.db import models
from django.db.models.signals import post_save
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.analysis_module.analysis_tool import AnalysisTool
from footprint.main.models.presentation.layer import Layer
from footprint.main.models.presentation.layer_library import LayerLibrary
from footprint.main.models.presentation.tilestache_config import TileStacheConfig
from footprint.main.models.analysis_module.environmental_constraint_module.environmental_constraint_percent import \
    EnvironmentalConstraintPercent
from footprint.main.models.geospatial.db_entity import DbEntity
from footprint.main.models.geospatial.behavior import BehaviorKey
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey
from footprint.main.utils.subclasses import receiver_subclasses
from footprint.main.utils.uf_toolbox import execute_sql, create_sql_calculations
from footprint.main.utils.utils import parse_schema_and_table
import logging

logger = logging.getLogger(__name__)

__author__ = 'calthorpe'

class EnvironmentalConstraintUpdaterTool(AnalysisTool):

    db_entities = models.ManyToManyField(DbEntity, through=EnvironmentalConstraintPercent)
    objects = GeoInheritanceManager()

    class Meta(object):
        app_label = 'main'
        abstract = False

    _no_post_save_publishing = False

    @classmethod
    def pre_save(cls, user_id, **kwargs):
        EnvironmentalConstraintUpdaterTool._no_post_save_publishing = True

    @classmethod
    def post_save(cls, user_id, objects, **kwargs):
        EnvironmentalConstraintUpdaterTool._no_post_save_publishing = False
        # Save to kick off the post save processing
        for obj in objects:
            obj.save()

    def initialize(self, created):
        """
            Upon initialization, we run the tool's update method if the tool was just created or no DbEntities
            are yet registered
        """
        self.update()

    def update(self):

        base_table = self.config_entity.db_entity_feature_class(
            DbEntityKey.BASE)

        developable_feature_class = self.config_entity.db_entity_feature_class(
            DbEntityKey.DEVELOPABLE)

        options = dict(
            project_schema=parse_schema_and_table(base_table._meta.db_table)[0],
            scenario_schema=parse_schema_and_table(developable_feature_class._meta.db_table)[0],
            developable_table=developable_feature_class.db_entity_key
        )

        current_db_entities, db_entities_to_add, db_entities_to_delete = \
            self.update_or_create_environmental_constraint_percents(self.config_entity)

        current_environmental_constraints = []
        for db_entity in current_db_entities:
            constraint_class = self.config_entity.db_entity_feature_class(db_entity.key)
            environmental_constraint_percent = EnvironmentalConstraintPercent.objects.filter(
                db_entity_id=db_entity.id,
                analysis_tool_id=self.id)[0]
            current_environmental_constraints.append(
                dict(
                    key=constraint_class.db_entity_key,
                    priority=environmental_constraint_percent.priority,
                    percent=environmental_constraint_percent.percent
                )
            )

        pSql = '''
        DO $$
            BEGIN
                BEGIN
                    ALTER TABLE {project_schema}.environmental_constraint_geographies_table_unioned ADD COLUMN constraint_acres_{config_entity_id} float;
                EXCEPTION
                    WHEN duplicate_column
                        THEN -- do nothing;
                END;
            END;
        $$'''.format(
            project_schema=options['project_schema'],
            config_entity_id=self.config_entity.id
        )
        execute_sql(pSql)

        logger.info('Calculate constraint acreage for the active scenario developable feature')
        for db_entity in current_db_entities:
            constraint_class = self.config_entity.db_entity_feature_class(db_entity.key)
            environmental_constraint_percent = EnvironmentalConstraintPercent.objects.filter(
                db_entity_id=db_entity.id,
                analysis_tool_id=self.id)[0]
            constraint_percent = environmental_constraint_percent.percent
            active_constraint = filter(lambda dct: constraint_class.db_entity_key in dct['key'], current_environmental_constraints)[0]
            priority_constraints = filter(lambda dct: dct['priority'] < active_constraint['priority'] or (dct['priority'] == active_constraint['priority'] and dct['percent'] > active_constraint['percent']), current_environmental_constraints)

            priority_key_list = []
            for constraint in priority_constraints:
                priority_key_list.append(constraint['key'])

            priority_query = create_sql_calculations(priority_key_list, ' and {0}_id is null', ' and a.primary_id is not null')

            pSql = '''
            update {project_schema}.environmental_constraint_geographies_table_unioned a set
                constraint_acres_{config_entity_id} = acres * {percent} where {constraint}_id = {constraint_id} {priority_query};
            '''.format(
                project_schema=options['project_schema'],
                constraint=constraint_class.db_entity_key,
                constraint_id=db_entity.id,
                percent=constraint_percent,
                priority_query=priority_query,
                config_entity_id=self.config_entity.id
            )

            execute_sql(pSql)

        pSql = '''
        update {scenario_schema}.{developable_table} a set
            acres_developable = a.acres_gross - b.constraint_acres
            FROM
            (select primary_id,
                    sum(constraint_acres_{config_entity_id}) as constraint_acres
                from {project_schema}.environmental_constraint_geographies_table_unioned
                    where constraint_acres_{config_entity_id} is not null group by primary_id) b
        where a.id= b.primary_id;
        '''.format(
            scenario_schema=options['scenario_schema'],
            project_schema=options['project_schema'],
            developable_table=options['developable_table'],
            config_entity_id=self.config_entity.id
        )

        execute_sql(pSql)

        pSql = '''
        update {scenario_schema}.{developable_table} set developable_index = (case when acres_gross > 0 then acres_developable / acres_gross else 0 end)
        '''.format(
            scenario_schema=options['scenario_schema'],
            developable_table=options['developable_table']
        )
        execute_sql(pSql)

        layer_libraries = LayerLibrary.objects.filter(config_entity=self.config_entity)
        layers = Layer.objects.filter(presentation__in=layer_libraries, db_entity_key__in=[DbEntityKey.DEVELOPABLE])
        # Invalidate these layers
        from footprint.main.publishing.tilestache_publishing import invalidate_cache
        for layer in layers:
            invalidate_cache(layer, TileStacheConfig.objects.get().config)

    def update_or_create_environmental_constraint_percents(self, config_entity):
        
        previous_db_entities = set(filter(lambda db_entity: db_entity.is_valid, self.db_entities.all()))
        current_db_entities = \
            set(filter(lambda db_entity: db_entity.is_valid, config_entity.db_entities_having_behavior_key(BehaviorKey.Fab.ricate('environmental_constraint'))))

        db_entities_to_add = current_db_entities - previous_db_entities
        analysis_tool = EnvironmentalConstraintUpdaterTool.objects.get(
            config_entity=config_entity
        )
        
        db_entities_to_delete = previous_db_entities - current_db_entities
        analysis_tool.environmentalconstraintpercent_set.filter(
            db_entity__in=db_entities_to_delete).delete()
        
        for db_entity in db_entities_to_add:
            if db_entity.is_valid:
                # add new environmental constraints to the environmental constraint rows
                EnvironmentalConstraintPercent.objects.create(
                    db_entity=db_entity,
                    analysis_tool=analysis_tool,
                    percent=1)

        active_db_entities = current_db_entities - db_entities_to_delete

        return active_db_entities, db_entities_to_add, db_entities_to_delete

# TODO should be handled by based class but isn't
@receiver_subclasses(post_save, EnvironmentalConstraintUpdaterTool, "on_environmental_constraint_updater_tool_post_save")
def on_analysis_tool_post_save(sender, **kwargs):
    analysis_tool = kwargs['instance']

    if not analysis_tool._no_post_save_publishing:
        analysis_tool.update()