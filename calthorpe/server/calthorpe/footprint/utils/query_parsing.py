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
from django.db.models import Q
from footprint.lib.functions import deep_map_dict_structure

COMPARISON_LOOKUP = {
    '<': 'lt',
    '<=': 'lte',
    '>': 'gt',
    '>=': 'gte'
    # TODO fill this out
    #BEGINS_WITH -- (checks if a string starts with another one)
    #ENDS_WITH -- (checks if a string ends with another one)
    #CONTAINS -- (checks if a string contains another one, or if an object is in an array)
    #MATCHES -- (checks if a string is matched by a regexp, you will have to use a parameter to insert the regexp)
    #ANY -- (checks if the thing on its left is contained in the array on its right, you will have to use a parameter to insert the array)
    #TYPE_IS -
}

def parse_query(manager, query, joins=None):
    objects = manager #.select_related('geography')
    join_queryset = []
    if joins:
        model = manager.model
        for join in joins:
            join_feature_class = model.config_entity.feature_class_of_db_entity(join)
            # Replace the uses of a db_entity_key for a table name with an unqualified column
            join_query = deep_map_dict_structure(query, {
                basestring: lambda value: value.replace(join+'.', '')
            })
            join_queryset.append(join_feature_class.objects.filter(parse_token(join_query)))
            # setup initial FROM clause
            # OR contacts.query.get_initial_alias()
            #alias = objects.query.join((None, model._meta.db_table, None, None))

            # Join the feature_class by the geography
            #connection = (
            #    model.geography.field.rel.to._meta.db_table,
            #    join_feature_class._meta.db_table,
            #    model.geography.field.rel.to._meta.pk.column,
            #    'geography_id'
            #)
            #alias = objects.query.join(connection)
            # select the join_feature_class fields
            #objects.extra(
            #    where={alias: '{0}.*'.format(alias)}
            #)
            # Replace query feature db_entity_key based table name with full name
            #query = deep_map_dict_structure(query, {
            #    basestring: lambda value: value.replace(join, join_feature_class._meta.db_table)
            #})
    if len(join_queryset) > 0:
        queryset = objects
        for join_queryset in join_queryset:
            # Fake an inner join by matching the joined query set on feature.geography.id
            queryset = queryset.filter(geography__in=map(lambda feature: feature.geography, join_queryset))
        return queryset
    else:
        return objects.filter(parse_token(query))

def parse_token(token):

    token_type = token['tokenType']
    left_side = token.get('leftSide', None)
    right_side = token.get('rightSide', None)

    if token_type == 'AND':
        left_side_result = parse_token(left_side)
        right_side_result = parse_token(right_side)
        return  [left_side_result, right_side_result]
    elif token_type == 'OR':
        left_side_result = parse_token(left_side)
        right_side_result = parse_token(right_side)
        return ' | '.join([left_side_result, right_side_result])
    # TODO handle NOT with ~Q()
    elif token_type in ['<', '>']:
        return Q(**{'{0}__{1}'.format(parse_simple_token(left_side), COMPARISON_LOOKUP[token_type]):
                    parse_simple_token(right_side)})
    elif token_type == '=':
        return Q(**{parse_simple_token(left_side):
                    parse_simple_token(right_side)})
    elif token_type == '!=':
        return Q(**{parse_simple_token(left_side):
                        parse_simple_token(right_side)})
    # TODO handle other operators
    return {}

def parse_simple_token(token):
    if token['tokenType'] == 'PROPERTY':
        return '__'.join(token['tokenValue'].split('.'))
    elif token['tokenType'] == 'NUMBER':
        return float(token['tokenValue'])
    elif token['tokenType'] == 'STRING':
        return token['tokenValue']
    # TODO handle booleans and other types
    return token['tokenType']


