import time
from footprint.celery import app
from footprint.common.utils.websockets import send_message_to_client
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.tasks.async_job import Job
from footprint.main.models.analysis_module.analysis_module import AnalysisModule
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
import logging
from footprint.main.models.keys.keys import Keys

__author__ = 'calthorpe_associates'


logger = logging.getLogger(__name__)

class Fiscal(AnalysisModule):

    objects = GeoInheritanceManager()

    def start(self):
        job = Job.objects.create(
            type="fiscal",
            status="New",
            user=self.user
        )
        job.save()

        task = executeFiscal.apply_async(
            args=[job.hashid, self.user, self.config_entity],
            soft_time_limit=3600,
            time_limit=3600,
            countdown=1
        )
        job = Job.objects.get(hashid=job.hashid)
        job.task_id = task.id

    class Meta(object):
        app_label = 'main'


@app.task
def executeFiscal(hash_id, user, config_entity):
    # Make sure all related models have been created before querying
    FeatureClassCreator(config_entity).ensure_dynamic_models()
    logger.info("Executing Fiscal using {0}".format(config_entity))
    run_fiscal_calculations(config_entity)
    logger.info("Done executing Fiscal")
    logger.info("Executed Fiscal using {0}".format(config_entity))
    send_message_to_client(user.id,
                           dict(event='FiscalModelCompleted',
                                config_entity_id=config_entity.id)
    )

def run_fiscal_calculations(config_entity):
    start_time = time.time()

    policy_assumptions = {}

    #Operations and Maintenance assumptions passed from the active scenario policy set
    policy_assumptions['urban_operations_maintenance_sfll'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.operations_maintenance_costs.urban.single_family_large_lot'))
    policy_assumptions['urban_operations_maintenance_sfsl'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.operations_maintenance_costs.urban.single_family_small_lot'))
    policy_assumptions['urban_operations_maintenance_attsf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.operations_maintenance_costs.urban.single_family_attached'))
    policy_assumptions['urban_operations_maintenance_mf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.operations_maintenance_costs.urban.multifamily'))

    policy_assumptions['compact_refill_operations_maintenance_sfll'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.operations_maintenance_costs.compact_refill.single_family_large_lot'))
    policy_assumptions['compact_refill_operations_maintenance_sfsl'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.operations_maintenance_costs.compact_refill.single_family_small_lot'))
    policy_assumptions['compact_refill_operations_maintenance_attsf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.operations_maintenance_costs.compact_refill.single_family_attached'))
    policy_assumptions['compact_refill_operations_maintenance_mf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.operations_maintenance_costs.compact_refill.multifamily'))

    policy_assumptions['compact_greenfield_operations_maintenance_sfll'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.operations_maintenance_costs.compact_greenfield.single_family_large_lot'))
    policy_assumptions['compact_greenfield_operations_maintenance_sfsl'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.operations_maintenance_costs.compact_greenfield.single_family_small_lot'))
    policy_assumptions['compact_greenfield_operations_maintenance_attsf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.operations_maintenance_costs.compact_greenfield.single_family_attached'))
    policy_assumptions['compact_greenfield_operations_maintenance_mf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.operations_maintenance_costs.compact_greenfield.multifamily'))

    policy_assumptions['standard_operations_maintenance_sfll'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.operations_maintenance_costs.standard.single_family_large_lot'))
    policy_assumptions['standard_operations_maintenance_sfsl'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.operations_maintenance_costs.standard.single_family_small_lot'))
    policy_assumptions['standard_operations_maintenance_attsf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.operations_maintenance_costs.standard.single_family_attached'))
    policy_assumptions['standard_operations_maintenance_mf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.operations_maintenance_costs.standard.multifamily'))

    #Revenue assumptions passed from the active scenario policy set
    policy_assumptions['urban_revenue_sfll'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.revenue.urban.single_family_large_lot'))
    policy_assumptions['urban_revenue_sfsl'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.revenue.urban.single_family_small_lot'))
    policy_assumptions['urban_revenue_attsf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.revenue.urban.single_family_attached'))
    policy_assumptions['urban_revenue_mf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.revenue.urban.multifamily'))

    policy_assumptions['compact_refill_revenue_sfll'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.revenue.compact_refill.single_family_large_lot'))
    policy_assumptions['compact_refill_revenue_sfsl'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.revenue.compact_refill.single_family_small_lot'))
    policy_assumptions['compact_refill_revenue_attsf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.revenue.compact_refill.single_family_attached'))
    policy_assumptions['compact_refill_revenue_mf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.revenue.compact_refill.multifamily'))

    policy_assumptions['compact_greenfield_revenue_sfll'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.revenue.compact_greenfield.single_family_large_lot'))
    policy_assumptions['compact_greenfield_revenue_sfsl'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.revenue.compact_greenfield.single_family_small_lot'))
    policy_assumptions['compact_greenfield_revenue_attsf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.revenue.compact_greenfield.single_family_attached'))
    policy_assumptions['compact_greenfield_revenue_mf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.revenue.compact_greenfield.multifamily'))

    policy_assumptions['standard_revenue_sfll'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.revenue.standard.single_family_large_lot'))
    policy_assumptions['standard_revenue_sfsl'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.revenue.standard.single_family_small_lot'))
    policy_assumptions['standard_revenue_attsf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.revenue.standard.single_family_attached'))
    policy_assumptions['standard_revenue_mf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.revenue.standard.multifamily'))

    #Capital Cost assumptions passed from the active scenario policy set
    policy_assumptions['urban_capital_sfll'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.capital_costs.urban.single_family_large_lot'))
    policy_assumptions['urban_capital_sfsl'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.capital_costs.urban.single_family_small_lot'))
    policy_assumptions['urban_capital_attsf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.capital_costs.urban.single_family_attached'))
    policy_assumptions['urban_capital_mf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.capital_costs.urban.multifamily'))

    policy_assumptions['compact_refill_capital_sfll'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.capital_costs.compact_refill.single_family_large_lot'))
    policy_assumptions['compact_refill_capital_sfsl'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.capital_costs.compact_refill.single_family_small_lot'))
    policy_assumptions['compact_refill_capital_attsf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.capital_costs.compact_refill.single_family_attached'))
    policy_assumptions['compact_refill_capital_mf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.capital_costs.compact_refill.multifamily'))

    policy_assumptions['compact_greenfield_capital_sfll'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.capital_costs.compact_greenfield.single_family_large_lot'))
    policy_assumptions['compact_greenfield_capital_sfsl'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.capital_costs.compact_greenfield.single_family_small_lot'))
    policy_assumptions['compact_greenfield_capital_attsf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.capital_costs.compact_greenfield.single_family_attached'))
    policy_assumptions['compact_greenfield_capital_mf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.capital_costs.compact_greenfield.multifamily'))

    policy_assumptions['standard_capital_sfll'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.capital_costs.standard.single_family_large_lot'))
    policy_assumptions['standard_capital_sfsl'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.capital_costs.standard.single_family_small_lot'))
    policy_assumptions['standard_capital_attsf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.capital_costs.standard.single_family_attached'))
    policy_assumptions['standard_capital_mf'] = float(config_entity.selected_policy_set().\
        policy_by_key('fiscal.capital_costs.standard.multifamily'))

    scenario_time_increment = float(config_entity.year - config_entity.project.base_year)
    fiscal_feature_class = config_entity.db_entity_feature_class(Keys.DB_ABSTRACT_FISCAL_FEATURE, base_class=True)
    net_increment_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_INCREMENT_FEATURE)

    features = net_increment_class.objects.filter(land_development_category__isnull = False)

    fiscal_outputs = []

    for feature in features:
        new_feature = fiscal_feature_class()
        new_feature.id = feature.id
        new_feature.residential_capital_costs = calculate_residential_capital_costs(feature, policy_assumptions)
        new_feature.residential_operations_maintenance_costs = calculate_residential_operations_maintenance_costs\
            (feature, policy_assumptions, scenario_time_increment)
        new_feature.residential_revenue = calculate_residential_revenue(feature, policy_assumptions)
        new_feature.wkb_geometry = feature.wkb_geometry

        fiscal_outputs.append(new_feature)

    fiscal_feature_class.objects.all().delete()
    fiscal_feature_class.objects.bulk_create(fiscal_outputs)

    print 'Finished: ' + str(time.time() - start_time)

    from footprint.main.publishing.config_entity_publishing import post_save_config_entity_analytic_run
    post_save_config_entity_analytic_run.send(sender=config_entity.__class__, config_entity=config_entity, module='fiscal')


def calculate_residential_capital_costs(feature, policy_assumptions):

    if feature.land_development_category == 'urban':
        residential_capital_costs = (float(feature.du_detsf_ll) * policy_assumptions['urban_capital_sfll']) + (float(feature.du_detsf_sl) * policy_assumptions['urban_capital_sfsl']) + (float(feature.du_attsf) * policy_assumptions['urban_capital_attsf']) + (float(feature.du_mf) * policy_assumptions['urban_capital_mf'])
        return residential_capital_costs

    elif feature.land_development_category == 'compact' and feature.refill_flag == True:
        residential_capital_costs = (float(feature.du_detsf_ll) * policy_assumptions['compact_refill_capital_sfll']) + (float(feature.du_detsf_sl) * policy_assumptions['compact_refill_capital_sfsl']) + (float(feature.du_attsf) * policy_assumptions['compact_refill_capital_attsf']) + (float(feature.du_mf) * policy_assumptions['compact_refill_capital_mf'])
        return residential_capital_costs

    elif feature.land_development_category == 'compact' and feature.refill_flag == False:
        residential_capital_costs = float((feature.du_detsf_ll) * policy_assumptions['compact_greenfield_capital_sfll']) + float((feature.du_detsf_sl) * policy_assumptions['compact_greenfield_capital_sfsl']) + float((feature.du_attsf) * policy_assumptions['compact_greenfield_capital_attsf']) + float((feature.du_mf) * policy_assumptions['compact_greenfield_capital_mf'])
        return residential_capital_costs

    elif feature.land_development_category == 'standard':
        residential_capital_costs = (float(feature.du_detsf_ll) * policy_assumptions['standard_capital_sfll']) + (float(feature.du_detsf_sl) * policy_assumptions['standard_capital_sfsl']) + (float(feature.du_attsf) * policy_assumptions['standard_capital_attsf']) + (float(feature.du_mf) * policy_assumptions['standard_capital_mf'])

        return residential_capital_costs



def calculate_residential_operations_maintenance_costs(feature, policy_assumptions, scenario_time_increment):

    if feature.land_development_category == 'urban':
        residential_operation_maintenance_costs = ((float(feature.du_detsf_ll) * policy_assumptions['urban_operations_maintenance_sfll']) + (float(feature.du_detsf_sl) * policy_assumptions['urban_operations_maintenance_sfsl']) + (float(feature.du_attsf) * policy_assumptions['urban_operations_maintenance_attsf']) + (float(feature.du_mf) * policy_assumptions['urban_operations_maintenance_mf'])) * scenario_time_increment
        return residential_operation_maintenance_costs

    elif feature.land_development_category == 'compact' and feature.refill_flag == True:
        residential_operation_maintenance_costs = ((float(feature.du_detsf_ll) * policy_assumptions['compact_refill_operations_maintenance_sfll']) + (float(feature.du_detsf_sl) * policy_assumptions['compact_refill_operations_maintenance_sfsl']) + (float(feature.du_attsf) * policy_assumptions['compact_refill_operations_maintenance_attsf']) + (float(feature.du_mf) * policy_assumptions['compact_refill_operations_maintenance_mf'])) * scenario_time_increment
        return residential_operation_maintenance_costs

    elif feature.land_development_category == 'compact' and feature.refill_flag == False:
        residential_operation_maintenance_costs = ((float(feature.du_detsf_ll) * policy_assumptions['compact_greenfield_operations_maintenance_sfll']) + (float(feature.du_detsf_sl) * policy_assumptions['compact_greenfield_operations_maintenance_sfsl']) + (float(feature.du_attsf) * policy_assumptions['compact_greenfield_operations_maintenance_attsf']) + (float(feature.du_mf) * policy_assumptions['compact_greenfield_operations_maintenance_mf'])) * scenario_time_increment
        return residential_operation_maintenance_costs

    elif feature.land_development_category == 'standard':
        residential_operation_maintenance_costs = ((float(feature.du_detsf_ll) * policy_assumptions['standard_operations_maintenance_sfll']) + (float(feature.du_detsf_sl) * policy_assumptions['standard_operations_maintenance_sfsl']) + (float(feature.du_attsf) * policy_assumptions['standard_operations_maintenance_attsf']) + (float(feature.du_mf) * policy_assumptions['standard_operations_maintenance_mf'])) * scenario_time_increment
        return residential_operation_maintenance_costs



def calculate_residential_revenue(feature, policy_assumptions):

    if feature.land_development_category == 'urban':
        residential_revenue_costs = (float(feature.du_detsf_ll) * policy_assumptions['urban_revenue_sfll']) + (float(feature.du_detsf_sl) * policy_assumptions['urban_revenue_sfsl']) + (float(feature.du_attsf) * policy_assumptions['urban_revenue_attsf']) + (float(feature.du_mf) * policy_assumptions['urban_revenue_mf'])

    elif feature.land_development_category == 'compact' and feature.refill_flag == True:
        residential_revenue_costs = (float(feature.du_detsf_ll) * policy_assumptions['compact_refill_revenue_sfll']) + (float(feature.du_detsf_sl) * policy_assumptions['compact_refill_revenue_sfsl']) + (float(feature.du_attsf) * policy_assumptions['compact_refill_revenue_attsf']) + (float(feature.du_mf) * policy_assumptions['compact_refill_revenue_mf'])

    elif feature.land_development_category == 'compact' and feature.refill_flag == False:
        residential_revenue_costs = (float(feature.du_detsf_ll) * policy_assumptions['compact_greenfield_revenue_sfll']) + (float(feature.du_detsf_sl) * policy_assumptions['compact_greenfield_revenue_sfsl']) + (float(feature.du_attsf) * policy_assumptions['compact_greenfield_revenue_attsf']) + (float(feature.du_mf) * policy_assumptions['compact_greenfield_revenue_mf'])

    elif feature.land_development_category == 'standard':
        residential_revenue_costs = (float(feature.du_detsf_ll) * policy_assumptions['standard_revenue_sfll']) + (float(feature.du_detsf_sl) * policy_assumptions['standard_revenue_sfsl']) + (float(feature.du_attsf) * policy_assumptions['standard_revenue_attsf']) + (float(feature.du_mf) * policy_assumptions['standard_revenue_mf'])

    return residential_revenue_costs