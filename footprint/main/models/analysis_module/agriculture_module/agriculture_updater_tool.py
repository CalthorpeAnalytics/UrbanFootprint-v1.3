import datetime
from django.utils.timezone import utc
from footprint.common.utils.websockets import send_message_to_client
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.analysis_module.analysis_tool import AnalysisTool
from footprint.main.models.config.scenario import BaseScenario, FutureScenario
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey
from footprint.main.utils.query_parsing import annotated_related_feature_class_pk_via_geographies
from footprint.main.utils.utils import timestamp
import logging
logger = logging.getLogger(__name__)

__author__ = 'calthorpe'

class AgricultureUpdaterTool(AnalysisTool):

    objects = GeoInheritanceManager()

    class Meta(object):
        app_label = 'main'
        abstract = False

    def test_agriculture_core(self, **kwargs):
        self.agriculture_analysis(**kwargs)

    def progress(self, proportion, **kwargs):
        send_message_to_client(kwargs['user'].id, dict(
            event='postSavePublisherProportionCompleted',
            job_id=str(kwargs['job'].hashid),
            config_entity_id=self.config_entity.id,
            id=kwargs['analysis_module'].id,
            class_name='AnalysisModule',
            key=kwargs['analysis_module'].key,
            proportion=proportion)
        )
        logger.info("Progress {0}".format(proportion))

    def update(self, **kwargs):
        logger.info('{0}:Starting Agriculture Core Analysis for {1}'.format(timestamp(), self.config_entity))
        if isinstance(self.config_entity.subclassed_config_entity, BaseScenario):
            agriculture_db_entity_key = DbEntityKey.BASE_AGRICULTURE
            developable_db_entity_key = DbEntityKey.DEFAULT_DEVELOPABLE
        elif isinstance(self.config_entity.subclassed_config_entity, FutureScenario):
            agriculture_db_entity_key = DbEntityKey.FUTURE_AGRICULTURE
            developable_db_entity_key = DbEntityKey.DEVELOPABLE
        else:
            raise Exception("Config Entity is not a Future or Base Scenario, cannot run AgricultureCore.")

        agriculture_feature_class = self.config_entity.db_entity_feature_class(agriculture_db_entity_key)

        developable_class = self.config_entity.db_entity_feature_class(developable_db_entity_key)

        if kwargs.get('ids', None):
            features = agriculture_feature_class.objects.filter(id__in=kwargs['ids'])
        else:
            features = agriculture_feature_class.objects.all()

        unattributed_features = features.filter(built_form__isnull=True).update(
            built_form_key='', crop_yield=0, market_value=0, production_cost=0, water_consumption=0, labor_force=0,
            truck_trips=0,
            updated=datetime.datetime.utcnow().replace(tzinfo=utc)
        )
        logger.info("Set {0} rows = 0".format(unattributed_features))

        attributed_features = features.filter(built_form__isnull=False)
        feature_count = len(attributed_features)
        if not feature_count:
            logger.info("No features to process!")
            return
        logger.info("Annotating {0} features".format(feature_count))

        annotated_features = annotated_related_feature_class_pk_via_geographies(attributed_features, self.config_entity, [
            developable_db_entity_key])

        #todo: run this as a task to allow the table to be split up
        # arguments = map(lambda f: (f, developable_class, getattr(feature, developable_db_entity_key)), annotated_features)
        # result = update_features.chunks(arguments, 1000).group().apply_async()
        # print result[0].__dict__

        feature_number = 1
        logger.info("Processing {0} features...".format(feature_count))
        iterator_start = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.progress(0.1, **kwargs)

        for feature in annotated_features:
            # update_progress(self.config_entity, feature_number, feature_count, iterator_start, **kwargs)
            developable_id = getattr(feature, developable_db_entity_key)
            developable = developable_class.objects.get(id=developable_id)
            acres = developable.acres_parcel
            applied_acres = float(acres * feature.density_pct * feature.dev_pct)
            agriculture_attribute_set = feature.built_form.resolve_built_form(feature.built_form).agriculture_attribute_set
            feature.built_form_key = feature.built_form.key
            feature.crop_yield = agriculture_attribute_set.crop_yield * applied_acres
            feature.market_value = agriculture_attribute_set.unit_price * feature.crop_yield
            feature.production_cost = agriculture_attribute_set.cost * applied_acres
            feature.water_consumption = agriculture_attribute_set.water_consumption * applied_acres
            feature.labor_force = agriculture_attribute_set.labor_input * applied_acres
            feature.truck_trips = agriculture_attribute_set.truck_trips * applied_acres
            feature.dirty_flag = False
            feature.updated = iterator_start
            # requires django 1.5
            #feature.save(update_fields=['built_form_key', 'crop_yield', 'unit_price',
            #                             'cost', 'water_consumption', 'labor_input', 'truck_trips', 'dirty_flag', 'updated'])
            feature.save()
            feature_number += 1
        total_time = datetime.datetime.utcnow().replace(tzinfo=utc) - iterator_start

        logger.info("Processed {0} features in {1}: \t {2} per feature".format(
            feature_count, total_time, total_time/feature_count
        ))
        self.progress(.9, **kwargs)
        logger.info('{0}:Finished Agriculture Core Analysis for {1} '.format(timestamp(), self.config_entity))


    def update_progress(self, number, total, start, **kwargs):
        if total < 20:
            parts = float(total)
        else:
            parts = 20
        chunk = float(total) / parts
        increment = 1 / parts
        if number % chunk < 1:
            progress_value = float(number) / float(total)
            octotherps = int(round(progress_value * parts))
            spaces = parts - octotherps
            bar = '#'*octotherps + ' '*spaces
            print '\r[{0}] {1}%'.format(bar, round(progress_value*100, 2)) + " | " + \
                  self.estimated_time_remaining(progress_value, start) + " remaining"
        else:
            return


    def estimated_time_remaining(self, progress, start):
        current_time = datetime.datetime.utcnow().replace(tzinfo=utc)
        elapsed = current_time - start
        total_time = (elapsed * int(round((10/progress)))) / 10
        remaining_estimate = total_time - elapsed
        return str(remaining_estimate)