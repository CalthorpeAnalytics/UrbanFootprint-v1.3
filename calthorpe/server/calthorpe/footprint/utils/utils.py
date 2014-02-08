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
import inspect

from io import open
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Manager, get_model
import datetime
from django.db.models.fields.related import ReverseManyRelatedObjectsDescriptor
import os
from subprocess import Popen, PIPE, STDOUT
from django.db import connections
from os import path
from footprint.lib.functions import merge, map_to_dict, flatten
from django.conf import settings
from shapely.geometry import LineString
from django.contrib.gis.geos import MultiPolygon, Polygon, LinearRing

def decimal_constant_factory(value):
    return lambda: 0.0000000000

def import_json_file(path):
    return open(path).read().replace('\n', '').replace('\t', '')

def resolve_model(class_path):
    """
    Resolves a class path to a Django model class
    :param class_path: a string model class path
    :return:
    """
    return get_model(*class_path.split('.', 1))

def getSRIDForTable(db, table_name):
    cur = connections[db].cursor()
    sql = 'select st_srid(wkb_geometry) from ' + table_name + ' LIMIT 1'
    cur.execute(sql)
    result = cur.fetchall()

    return result[0][0]

def parse_schema_and_table(full_table_name):
    """
    Returns the database schema and table by parsing a full table name of the form "schema"."table"
    """
    return map(lambda str: strip_quotes(str), full_table_name.split('.'))


def strip_quotes(str):
    return str[1:-1] if str[0] == '"' else str


def table_name_only(dynamic_class):
    return dynamic_class._meta.db_table


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None

def update_and_return_dict(dict1,dict2):
    dict1.update(dict2)
    return dict1

def get_or_none_from_queryset(queryset, **kwargs):
    try:
        return queryset.get(**kwargs)
    except Exception, E:
        return None


def timestamp():
    """returns a formatted timestamp with detail of the hour and minute"
    """
    def make_character_string(time_unit):
        return str(time_unit) if len(str(time_unit)) == 2 else "0{0}".format(time_unit)

    now = datetime.datetime.now()
    time = dict(
        year=now.year,
        month=make_character_string(now.month),
        day=make_character_string(now.day),
        hour=make_character_string(now.hour),
        minute=make_character_string(now.minute)
    )

    timestamp = "{year}{month}{day}_{hour}{minute}".format(**time)
    return timestamp

## {{{ http://code.activestate.com/recipes/410469/ (r5)
class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''

    def __init__(self, parent_element):
        childrenNames = []
        for child in parent_element.getchildren():
            childrenNames.append(child.tag)

        if parent_element.items(): #attributes
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                #print len(element), element[0].tag, element[1].tag
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlListConfig(element)}
                    # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))

                if childrenNames.count(element.tag) > 1:
                    try:
                        currentValue = self[element.tag]
                        currentValue.append(aDict)
                        self.update({element.tag: currentValue})
                    except: #the first of its kind, an empty list must be created
                        self.update({element.tag: [aDict]}) #aDict is written in [], i.e. it will be a list

                else:
                    self.update({element.tag: aDict})
                    # this assumes that if you've got an attribute in a tag,
                    # you won't be having any text. This may or may not be a
                    # good idea -- time will tell. It works for the way we are
                    # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})

## end of http://code.activestate.com/recipes/410469/ }}}

def create_media_subdir(relative_path):
    subdir = path.join(settings.MEDIA_ROOT, relative_path)
    if not os.path.exists(subdir):
        os.makedirs(subdir)


def create_static_content_subdir(relative_path):
    subdir = path.join(settings.STATIC_ROOT, relative_path)
    if not os.path.exists(subdir):
        os.makedirs(subdir)


def save_media_file(output_file, file_content):
    #work around for Django bug where ContentFile does not support unicode
    outputfilename = path.join(settings.MEDIA_ROOT, output_file)
    f = open(outputfilename, "w")
    f.write(file_content)
    f.close()
    return outputfilename


def string_not_empty(str, default):
    return str if str != None and str != '' and str != u'' else default


def execute(command_and_args):
    p = Popen(command_and_args, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=False)
    return p.communicate()


def execute_with_stdin(command_and_args, stdin):
    """
        Executes a system command that requires input given to STDIN, such as psql
        Returns a tuple (stdout, stderr)
    """
    p = Popen(command_and_args, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=False)
    return p.communicate(input=stdin)


def execute_piped_with_stdin(commands_with_args, stdin):
    """
        Executes a system command piped to another system command where one or both require input from STDIN, such as pg_dump | psql
        Returns a tuple (stdout, stderr)
    """
    p1 = Popen(commands_with_args[0], stdout=PIPE)
    p2 = p1
    for command_with_args in commands_with_args[1:]:
        p2 = Popen(command_with_args, stdin=p2.stdout, stdout=PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    return p2.communicate(input="\n".join(stdin))


def load_template_source(path):
    # TODO this should work for any templates dir
    with open("{0}/{1}/{2}".format(settings.ROOT_PATH, 'footprint/templates', path), 'r') as f:
        return f.read()


def database_settings(db):
    connection = connections[db]
    return connection.settings_dict


def connection_dict(db):
    database = database_settings(db)
    return dict(
        host=database['HOST'],
        dbname=database['NAME'],
        user=database['USER'],
        password=database['PASSWORD'],
        port=5432
    )


def database_connection_string(db):
    settings = database_settings(db)
    return "db_name=%s host=%s user=%s password=%s" % (
        settings['NAME'], settings['HOST'], settings['USER'], settings['PASSWORD'])


def database_connection_string_for_pys(db):
    settings = database_settings(db)
    return "dbname=%s host=%s user=%s password=%s" % (
        settings['NAME'], settings['HOST'], settings['USER'], settings['PASSWORD'])


def database_connection_string_for_ogr(db):
    settings = database_settings(db)
    return "dbname=\'%s\' host=\'%s\' port=\'%s\' user=\'%s\' password=\'%s\' " % (
        settings['NAME'], settings['HOST'], settings['PORT'], settings['USER'], settings['PASSWORD']
    )


def to_tuple(point):
    """
        Convert the Shapely class to a tuple for use by GeoDjango.
        TODO figure out why GeoDjango interpolate methods don't exist
    :param point:
    :return:
    """
    return point.x, point.y


def chop_geom(multipolygon, fraction):
    """
        Transforms each point fraction the distance to the geometry's centroid to form a smaller geometry
    :param geom:
    :return: a multipolygon reduced by the fraction from the original
    """

    def transform_polygon(polygon):
        def transform_linear_ring(linear_ring):
            centroid = polygon.centroid
            return LinearRing(
                map(lambda point: to_tuple(LineString((point, centroid)).interpolate(fraction, normalized=True)),
                    linear_ring))

        linear_rings = map(lambda linear_ring: transform_linear_ring(linear_ring), polygon)
        if len(linear_rings) > 1:
            return Polygon(linear_rings[0], [linear_rings[1:]])
        else:
            return Polygon(linear_rings[0], [])

    return MultiPolygon(map(lambda polygon: transform_polygon(polygon), multipolygon))


def has_explicit_through_class(instance, attribute):
    """
        Returns through if this Many attribute has an explicit Through class
    :param instance: The instance or class containing the attribute
    :param attribute: A string representing the attribute
    :return: True if an explicit through class exists, False otherwise
    """
    field = getattr(instance, attribute)
    if isinstance(field, ReverseManyRelatedObjectsDescriptor):
        # If instance is a Model class
        return not field.through._default_manager.__class__ == Manager
        # Instance is a model instance
    return not hasattr(field, 'add')


def foreign_key_field_of_related_class(model_class, related_model_class):
    """
        For a model class, returns the foreign key ModelField of the given related_model_class. It's assumed that the model class doesn't define multiple foreign keys of the same type--that there is one foreign key for each of the two associated classes. related_model class can either match or be a subclass of the sought field rel.to class should
    :param model_class:
    :param related_model_class: The class or a subclass of the foreign key to match
    :return: the ForeignKey Field of the given class_of_foreign_key
    """
    fields = filter(
        lambda field: field.rel and (
            field.rel.to == related_model_class or issubclass(related_model_class, field.rel.to)),
        model_class._meta.fields)
    if len(fields) == 1:
        return fields[0]
    else:
        raise Exception(
            "For through class {0}, expected exactly one field with to class {1}, but got {2}".format(model_class,
                                                                                                      related_model_class,
                                                                                                      len(fields)))


def resolve_attribute(instance, attribute_parts):
    """
        Given attribute segments (perhaps created by splitting a django query attribute string (e.g. 'foo__id'), resolve the value of the attribute parts
    :param instance:
    :param attribute_parts: a list of string attribute
    :return: whatever the attribute_parts resolve to by digging into the given instance
    """
    return resolve_attribute(
        getattr(instance, attribute_parts[0]) if hasattr(instance, attribute_parts[0]) else instance.get(
            attribute_parts[0], None),
        attribute_parts[1:]) if len(attribute_parts) > 0 else instance

# From http://stackoverflow.com/questions/1165352/fast-comparison-between-two-python-dictionary
class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """

    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def added(self):
        return self.set_current - self.intersect

    def removed(self):
        return self.set_past - self.intersect

    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])

    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])


def reduce_dict_to_difference(dct, comparison_dict, deep=True):
    """
        Given a dict dct and a similar dict comparison dict, return a new dict that only contains the key/values of dct that are different than comparison dict, whether it's a key not in comparison_dict or a matching key with a different value. Specify deep=True to do a deep comparison of internal dicts
        # TODO This could handle list comparison better for deep=True. Right now it just marks the lists as different if they are not equal
    :param dct:
    :param comparison_dict:
    :param deep: Default True, compares embedded dictionaries by recursing
    :return: A new dict containing the differences
    """
    differ = DictDiffer(dct, comparison_dict)
    return merge(
        # Find keys and key values changed at the top level
        map_to_dict(lambda key: [key, dct[key]], flatten([differ.added(), differ.changed()])),
        # If deep==True recurse on dictionaries defined on the values
        *map(lambda key: reduce_dict_to_difference(*map(lambda dictionary: dictionary[key], [dct, comparison_dict])),
             # recurse on inner each dict pair
             # Find just the keys with dict values
             filter(lambda key: isinstance(dct[key], dict), differ.unchanged())) if deep else {}
    )


import pickle


def get_pickling_errors(obj, seen=None):
    if seen == None:
        seen = []
    try:
        state = obj.__getstate__()
    except AttributeError:
        return
    if state == None:
        return
    if isinstance(state, tuple):
        if not isinstance(state[0], dict):
            state = state[1]
        else:
            state = state[0].update(state[1])
    result = {}
    for i in state:
        try:
            pickle.dumps(state[i], protocol=2)
        except pickle.PicklingError:
            if not state[i] in seen:
                seen.append(state[i])
                result[i] = get_pickling_errors(state[i], seen)
    return result


def call_if_function(obj, args):
    """
        Takes an object and calls it as a function with *args if it is a function. Else returnes obj
    :param obj:
    :param args:
    :return:
    """
    return obj(*args) if hasattr(obj, '__call__') else obj

def expect(instance, *args):
    """
        When initializing an instance, raise an ImproperlyConfigured exception if the given args are not set for the
        given instance. Not set means None or not sepecified
    :param instance:
    :param args:
    :return:
    """
    missing_args = filter(lambda arg: not getattr(instance, arg), args)
    if len(missing_args) > 0:
        raise ImproperlyConfigured("Expected arg(s) {0}".format(', '.join(missing_args)))


def test_pickle(xThing,lTested = []):
    import pickle
    if id(xThing) in lTested:
        return lTested
    sType = type(xThing).__name__
    print('Testing {0}...'.format(sType))

    if sType in ['type','int','str']:
        print('...too easy')
        return lTested
    if sType == 'dict':
        print('...testing members')
        for k in xThing:
            lTested = test_pickle(xThing[k],lTested)
        print('...tested members')
        return lTested
    if sType == 'list':
        print('...testing members')
        for x in xThing:
            lTested = test_pickle(x)
        print('...tested members')
        return lTested

    lTested.append(id(xThing))
    oClass = type(xThing)

    for s in dir(xThing):
        if s.startswith('_'):
            print('...skipping *private* thingy')
            continue
        #if it is an attribute: Skip it
        try:
            xClassAttribute = oClass.__getattribute__(oClass,s)
        except AttributeError:
            pass
        else:
            if type(xClassAttribute).__name__ == 'property':
                print('...skipping property')
                continue

        xAttribute = xThing.__getattribute__(s)
        print('Testing {0}.{1} of type {2}'.format(sType,s,type(xAttribute).__name__))
        #if it is a function make sure it is stuck to the class...
        if type(xAttribute).__name__ == 'function':
            raise Exception('ERROR: found a function')
        if type(xAttribute).__name__ == 'method':
            print('...skipping method')
            continue
        if type(xAttribute).__name__ == 'HtmlElement':
            continue
        if type(xAttribute) == dict:
            print('...testing dict values for {0}.{1}'.format(sType,s))
            for k in xAttribute:
                lTested = test_pickle(xAttribute[k])
                continue
            print('...finished testing dict values for {0}.{1}'.format(sType,s))

        try:
            oIter = xAttribute.__iter__()
        except AttributeError:
            pass
        except AssertionError:
            pass #lxml elements do this
        else:
            print('...testing iter values for {0}.{1} of type {2}'.format(sType,s,type(xAttribute).__name__))
            for x in xAttribute:
                lTested = test_pickle(x,lTested)
            print('...finished testing iter values for {0}.{1}'.format(sType,s))

        try:
            xAttribute.__dict__
        except AttributeError:
            pass
        else:
            #this attribute should be explored seperately...
            lTested = test_pickle(xAttribute,lTested)
            continue
        pickle.dumps(xAttribute)


    print('Testing {0} as complete object'.format(sType))
    pickle.dumps(xThing)
    return lTested
