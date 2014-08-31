# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2014 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# model: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
from copy import deepcopy
import string
from django.db.models import Q, Min, Count, F, DateTimeField, DateField, TimeField, Field
import sys
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.dateparse import parse_datetime, parse_date, parse_time
from footprint.main.lib.functions import to_list, map_to_dict, compact
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.main.utils.dynamic_subclassing import resolve_queryable_name_of_type
from footprint.main.utils.utils import clear_many_cache

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

ARITHMETIC_LOOKUP = {
    '+':'+',
    '-':'-',
    '*':'*',
    '/':'/',
    '**':'**',
    '^':'**'
}


def parse_query(config_entity, manager, filters=None, joins=None, aggregates=None, group_bys=None):
    queryset = manager
    group_by_values = None
    annotation_tuples = None

    # Make sure all related models have been created before querying
    FeatureClassCreator(config_entity).ensure_dynamic_models()

    # Any joins are db_entity_keys and resolve to feature classes of the config_entity
    related_models = map(lambda join: config_entity.db_entity_feature_class(join), joins or [])

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
            related_field_pk_path = resolve_field_path_via_geographies('pk', manager, [related_model])
            queryset = queryset.filter(**{'{0}__isnull'.format(related_field_pk_path):False})

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
    elif group_by_values:
        # If no annotations are specified, add in a count annotation to make the group by take effect
        # As long as we annotate a count of one we'll get the correct group_by, since django receives values(group_by1, group_by2, etc).annotate(count(group_by1))
        queryset = queryset.annotate(count=Count(group_by_values[0]))

    return queryset

def is_aggregate(annotation_function):
    #TODO
    return False

def resolve_related_model_path_via_geographies(manager, related_model):
    """
        Returns the query string path 'geogrpaphies__[field name of the related model form the main model]'
    """
    geography_class = manager.model.geographies.field.rel.to
    geography_related_field_name = resolve_queryable_name_of_type(geography_class, related_model)
    return 'geographies__%s' % geography_related_field_name

#TODO this all should be in the Manager
def model_fields(manager, fields):
    """
        Returns the fields of the main model that are filtered by fields, if specified
    """
    return filter(lambda field: not fields or field.name in fields,  manager.model._meta.fields)

def model_field_paths(model, exclude_field_types=(), fields=None):
    """
        Returns the field names of the main model.
    """
    return compact(map(
        lambda field: field.name if (not fields or field.name in fields) and not isinstance(field, exclude_field_types) else None,
        model._meta.fields))

def main_field_paths_to_fields(manager, exclude_field_types=(), fields=None):
    return map_to_dict(
        lambda field: [field.name, field] if \
            (not fields or field.name in fields) and \
            not isinstance(field, exclude_field_types) else \
            None,
        manager.model._meta.fields)

def related_field_paths(manager, related_model, exclude_field_types=(), fields=None, separator=None):
    """
        Iterates through the fields of the related model, appending each to the related model field name
        from the main model. Returns the list of related field paths.
    """
    related_field = resolve_related_model_path_via_geographies(manager, related_model)
    return compact(map(lambda field: string.replace('{0}__{1}'.format(related_field, field.name),
                                                    '__',
                                                    separator or '__') if \
        (not fields or field.name in fields) and \
        not isinstance(field, exclude_field_types) else \
        None,
                       related_model._meta.fields))


def _field_path_and_cloned_field(related_field, field, separator):
    field_path = string.replace('{0}__{1}'.format(related_field, field.name),
                           '__',
                           separator or '__')
    cloned_field = deepcopy(field)
    cloned_field.name = field_path
    return [field_path, cloned_field]

def related_field_paths_to_fields(manager, related_model, exclude_field_types=(), fields=None, separator=None):
    """
        Iterates through the fields of the related model, appending each to the related model field name
        from the main model. Returns the dict of related field paths as keys valued by the field.
        :param exclude_field_types. Optional tuple of Field classes that should be filtered out.
        :param separator: Optional separator with which to replace __ in the related_field_paths
    """
    related_field = resolve_related_model_path_via_geographies(manager, related_model)
    return map_to_dict(
        lambda field: _field_path_and_cloned_field(related_field,field, separator) if \
            (not fields or field.name in fields) and \
            not isinstance(field, exclude_field_types) else \
            None,
        related_model._meta.fields)

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
            resolved_field_path = field_path
        except:
            # See if the first segment matches the related_model db_entity_key
            first_segment = field_path.split('__')[0]
            if first_segment != model.db_entity_key:
                # If not, move on
                continue
            # Take all but the first segment
            resolved_field_path = '__'.join(field_path.split('__')[1:])
        # Success, find the path to this model from geographies
        geography_related_field_name = resolve_queryable_name_of_type(geography_class, model)
        return 'geographies__%s__%s' % (geography_related_field_name, resolved_field_path)
    # See if it matches the main model
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

def parse_token(token, manager, related_models, left=False, sibling_token=None):

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
        left_side_result = parse_token(left_side, manager, related_models, left=True)
        return Q(**{'{0}__{1}'.format(left_side_result, COMPARISON_LOOKUP[token_type]):
                    parse_token(right_side, manager, related_models, sibling_token=left_side)})
    elif token_type == '=':
        return Q(**{parse_token(left_side, manager, related_models, left=True):
                    parse_token(right_side, manager, related_models, sibling_token=left_side)})
    elif token_type == '!=':
        return ~Q(**{parse_token(left_side, manager, related_models, left=True):
                    parse_token(right_side, manager, related_models, sibling_token=left_side)})
    # TODO handle other operators
    elif token_type in ARITHMETIC_LOOKUP.keys():
        # TODO untested
        return eval('parse_token(left_side, manager, related_models)' +
                    'token_type' +
                    'parse_token(right_side, manager, related_models)')

    # If the token type isn't a complex operator, assume it's a primitive
    return parse_simple_token(token, manager, related_models, left=left, sibling_token=sibling_token)


def parse_simple_token(token, manager, related_models, left=False, sibling_token=None):
    """
        Parse the simple token dict.
        :param token: a dict with 'tokenType'=='PROPERTY'|'NUMBER'|'STRING'
            and 'tokenValue'==a value of the corresponding type.
        :param manager: The django model manager
        :param related_models: Related models joined to the manager model
        :param left: Default False. If set then the token is an assignee and shouldn't be wrapped in
        an F() expression if it's a property

    """
    if token['tokenType'] == 'PROPERTY':
        # Resolve the field path in case it's relative to a joined related_model
        field = resolve_field_path_via_geographies('__'.join(token['tokenValue'].split('.')), manager, related_models)
        # Wrap in an F() expression if field is a right-side argument (the thing being assigned)
        return field if left else F(field)
    elif token['tokenType'] == 'NUMBER':
        return float(token['tokenValue'])
    elif token['tokenType'] == 'STRING':
        value = token['tokenValue']
        if sibling_token and sibling_token.get('tokenType', None) == 'PROPERTY':
            field = resolve_field_path_via_geographies('__'.join(sibling_token['tokenValue'].split('.')), manager, related_models)
            parts = field.split('__')
            model = manager.model
            while len(parts) > 0:
                part = parts.pop()
                model_or_field_tuple = model._meta._name_map.get(part)
                if not model_or_field_tuple:
                    # Something went wrong, give up
                    return value
                model_or_field = model_or_field_tuple[0]
                parser_lookup = {DateTimeField: parse_datetime, DateField: parse_date, TimeField: parse_time}
                if isinstance(model_or_field, (DateTimeField, DateField, TimeField)):
                    date_time = parser_lookup[model_or_field.__class__](value)
                    if not date_time.tzinfo:
                        return date_time.replace(tzinfo=timezone.utc)
                    return date_time
        return value

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
        related_model = config_entity.db_entity_feature_class(db_entity_key)
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
