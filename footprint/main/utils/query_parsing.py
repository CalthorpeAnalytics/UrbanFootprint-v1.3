# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2013 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# model: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
from django.db.models import Q, Min
import sys
from django.contrib.gis.db.models.query import GeoQuerySet
from django.db.models.query import QuerySet
from django.template.defaultfilters import slugify
from footprint.main.lib.functions import deep_map_dict_structure, to_list, map_to_dict
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.main.utils.dynamic_subclassing import resolve_field, resolve_field_of_type, resolve_queryable_name_of_type
from footprint.main.utils.utils import full_module_path, clear_many_cache

COMPARISON_LOOKUP = {
    '<': 'lt',
    '<=': 'lte',
    '>': 'gt',
    '>=': 'gte',
    'BEGINS_WITH': 'startswith',
    'ENDS_WITH': 'endswith',
    'CONTAINS': 'contains' # TODO would be 'in' for SC Arrays
    #'MATCHES':
    #'ANY':
    #TYPE_IS -
}

def parse_query(config_entity, manager, filters=None, joins=None, aggregates=None, group_bys=None):
    queryset = manager
    group_by_values = None
    annotation_tuples = None

    # Make sure all related models have been created before querying
    FeatureClassCreator(config_entity).ensure_dynamic_models()

    # Any joins are db_entity_keys and resolve to feature classes of the config_entity
    related_models = map(lambda join: config_entity.feature_class_of_db_entity_key(join), joins or [])

    # Use group_by_values to group by and then attach the aggregates to each unique result via annotation
    # If aggregates are specified but group by is not, we use aggregate to just get a single result
    # For now we assume any filtering should be applied BEFORE aggregation
    if filters:
        queryset = queryset.filter(parse_token(filters, manager, related_models))

    # We only need to join explicitly if the join is not included in one of the group by fields
    manual_joins = joins or [] if not group_bys else \
        set(joins or [])-\
        set(map(lambda group_by: resolve_db_entity_key_of_field_path(parse_group_by(group_by, manager, related_models), manager, related_models), group_bys))

    if manual_joins:
        # If there are joins, filter the queryset by inner join on the related_model pk through geography
        for related_model in related_models:
            queryset = queryset.filter(**{'{0}__isnull'.format(resolve_field_path_via_geographies('pk', manager, [related_model])):False})

    # If there are aggregates, they are either part of the main table or join table
    if aggregates:
        # Resolve the field path using available joins via geographies or on the main model
        # Then send the resovled field
        annotation_tuples = map(
            lambda aggregate: parse_annotation(aggregate, manager, related_models),
            aggregates)
    if group_bys:
        group_by_values = map(
            lambda group_by: parse_group_by(group_by, manager, related_models),
            to_list(group_bys))

    if group_by_values:
        queryset = queryset.values(*group_by_values).order_by(*group_by_values)
    if annotation_tuples:
        if not group_by_values:
            queryset = [queryset.aggregate(*map(lambda annotation_tuple: annotation_tuple[0](annotation_tuple[1]), annotation_tuples))]
        else:
            for annotation_tuple in annotation_tuples:
                if isinstance(annotation_tuple[0], basestring):
                    # Chain named queryset methods
                    queryset = getattr(queryset, annotation_tuple[0])(annotation_tuple[1])
                else:
                    # Annotation built-in functions
                    queryset = queryset.annotate(annotation_tuple[0](annotation_tuple[1]))

    return queryset

def is_aggregate(annotation_function):
    #TODO
    return False

def resolve_field_path_via_geographies(field_path, manager, related_models):
    """
        Resolve the given field path in case its not absolute.
        For instance, if it is 'block' and one of our related models accessible via geographies__relatedmodel has that property,
        return 'geographies__relatedmodel__block'
        It will also be tested against the main manager after all related models fail,
        e.g. manager.values(field_path) if successful would simply return field_path
    :param field_path: django field path. e.g. du or built_form__name
    :param manager: The main manager by which the related models are resolved and by which the full path is computed
    :param related_models: models joined to the manager. For instance. manager.model is BaseFeature, a related_model could be
        CensusBlock, which might be related to the former via 'geographies__censusblock9rel'. The relationship is computed
        by assuming that the related model is related by geographies and looking for a field matching its type
    :return:
    """
    geography_class = manager.model.geographies.field.rel.to
    for model in related_models:
        try:
            # See if the field_name resolves
            # There's probably a more efficient way to do this
            model.objects.values(field_path)
        except:
            pass
        else:
            # Success, find the path to this model from geographies
            geography_related_field_name = resolve_queryable_name_of_type(geography_class, model)
            return 'geographies__%s__%s' % (geography_related_field_name, field_path)
    try:
        if field_path.split('__')[0] == manager.model.db_entity_key:
            # If the manager model db_entity_key was used in the path, just strip it out
            updated_field_path = '__'.join(field_path.split('__')[1:])
            manager.values(updated_field_path)
        else:
            # Otherwise test query with the full path
            updated_field_path = field_path
            manager.values(updated_field_path)
        # Success, return the field_path
        return updated_field_path
    except:
        raise Exception("Cannot resolve field path %s to the main model %s or any joined models %s" %
                        (field_path, manager.model, related_models))

def resolve_db_entity_key_of_field_path(field_path, manager, related_models):

    for related_model in related_models:
        try:
            # See if the field_name resolves
            # There's probably a more efficient way to do this
            related_model.objects.values(field_path)
            # Success, return the db_entity_key of the related_models
            return related_model.db_entity_key
        except:
            pass
    try:
        # If an absolute path, take the first segment and try to resolve it as a db_entity_key
        first_segment = field_path.split('__')
        try:
            if manager.model.config_entity.computed_db_entities(key=first_segment).count() > 0:
                return first_segment
        except:
            # Must be a main feature class field_path
            return manager.model.config_entity.db_entity_key_of_feature_class(manager.model)
    except:
        raise Exception("Cannot resolve field path %s to the main model %s or any joined models %s" %
                        (field_path, manager.model, related_models))


def parse_group_by(group_by_token, manager, related_models):
    """
    :param group_by_token:
    :return:
    """
    return parse_simple_token(group_by_token, manager, related_models)

def parse_annotation(aggregate_token, manager, related_models):
    """
        token in the form {rightSide: {tokenValue: field_name}, tokenValue: 'AVG|SUM|COUNT'}
    :param aggregate_token:
    :param manager: main Manager
    :param related_models: related models
    :return: the aggregate function to be passed to annotate() along with any others
    """
    function_or_name = resolve_annotation(manager, aggregate_token['tokenValue']) if aggregate_token.get('tokenValue', None) else None
    field = aggregate_token['rightSide']['tokenValue'] if 'rightSide' in aggregate_token else aggregate_token['tokenValue']
    resolved_field_path = resolve_field_path_via_geographies(
        field,
        manager,
        (related_models or []))
    return (function_or_name, resolved_field_path) if function_or_name else resolved_field_path

def parse_token(token, manager, related_models):

    token_type = token['tokenType']
    left_side = token.get('leftSide', None)
    right_side = token.get('rightSide', None)

    if token_type == 'AND':
        left_side_result = parse_token(left_side, manager, related_models)
        right_side_result = parse_token(right_side, manager, related_models)
        return left_side_result & right_side_result
    elif token_type == 'OR':
        left_side_result = parse_token(left_side, manager, related_models)
        right_side_result = parse_token(right_side, manager, related_models)
        return left_side_result | right_side_result
    # TODO handle NOT with ~Q()
    elif token_type in COMPARISON_LOOKUP.keys():
        return Q(**{'{0}__{1}'.format(parse_simple_token(left_side, manager, related_models), COMPARISON_LOOKUP[token_type]):
                    parse_simple_token(right_side, manager, related_models)})
    elif token_type == '=':
        return Q(**{parse_simple_token(left_side, manager, related_models):
                    parse_simple_token(right_side, manager, related_models)})
    elif token_type == '!=':
        return Q(**{parse_simple_token(left_side, manager, related_models):
                        parse_simple_token(right_side, manager, related_models)})
    # TODO handle other operators
    return {}

def parse_simple_token(token, manager, related_models):
    if token['tokenType'] == 'PROPERTY':
        # Resolve the field path in case it's relative to a joined related_model
        return resolve_field_path_via_geographies('__'.join(token['tokenValue'].split('.')), manager, related_models)
    elif token['tokenType'] == 'NUMBER':
        return float(token['tokenValue'])
    elif token['tokenType'] == 'STRING':
        return token['tokenValue']
    # TODO handle booleans and other types
    return token['tokenType']

def resolve_annotation(manager, annotation):
    class_name = annotation.lower().capitalize()
    if hasattr(sys.modules['django.db.models'], class_name):
        return getattr(sys.modules['django.db.models'], class_name)
    function_name = slugify(annotation.lower())
    if hasattr(manager, function_name):
        return function_name

def annotated_related_feature_class_pk_via_geographies(manager, config_entity, db_entity_keys):
    """
        To join a related model by geographic join
    """
    # Success, find the path to this model from geographies
    geography_class = manager.model.geographies.field.rel.to
    def resolve_related_model_pk(db_entity_key):
        related_model = config_entity.feature_class_of_db_entity_key(db_entity_key)
        try:
            geography_related_field_name = resolve_queryable_name_of_type(geography_class, related_model)
        except:
            # Sometimes the geography class hasn't had its fields cached properly. Fix here
            clear_many_cache(geography_class)
            geography_related_field_name = resolve_queryable_name_of_type(geography_class, related_model)

        return 'geographies__%s__pk' % (geography_related_field_name)

    pk_paths = map_to_dict(lambda db_entity_key:
        [db_entity_key, Min(resolve_related_model_pk(db_entity_key))],
        db_entity_keys)

    return manager.annotate(**pk_paths)
