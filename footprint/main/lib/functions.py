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

# This module stores common functional-style functions that are not class specific.
# They should operate on any type and have qualities such as chainable or passable as arguments to other functions
# Make sure you check out Python's functools and itertools to see if what you need already exists before you write it.
from inspect import isfunction
from itertools import chain

__author__ = 'calthorpe_associates'

import collections


def to_iterable(object,
                if_iterable=lambda object: object,
                if_uniterable=lambda object: [object],
                is_iterable=lambda object: is_iterable(object)):
    """
    Returns an array containing the argument if it is not already iterable.

    Keyword arguments:
        is_iterable -- You may optionally specify this lambda if the default is an insufficient test. (default isinstance(object, Collections.Iterable)) For example, if testing an object like a string that is already iterable, you may want to make a special is_iterable lambda that checks to see if the object is a string in an array or not
        if_iterable -- An optional lambda to specify a mapping of the object if already iterable (default returns object)
        if_uniterable -- An optional lambda to specify a mapping of the object if not iterable (default returns  [object])

    """
    return if_iterable(object) if is_iterable(object) else if_uniterable(object)


def is_list_or_tuple(object):
    return isinstance(object, (list, tuple))


def is_list_tuple_or_dict(object):
    return isinstance(object, (list, tuple, dict))

def to_list(object,
            if_list_or_tuple=lambda object: object,
            if_not_list_nor_tuple=lambda object: [object],
            is_list_or_tuple=is_list_or_tuple
):
    """
    Returns an array containing the argument if it is not already an array

    Keyword arguments:
        is_list_or_tuple -- You may optionally specify this lambda if the default is an insufficient test. (default isinstance(object, Array))
        if_list_or_tuple -- An optional lambda to specify a mapping of the object if already a list or tuple (default returns object)
        if_not_list_nor_tuple -- An optional lambda to specify a mapping of the object if not a list or tuple (default returns  [object])

    """
    return if_list_or_tuple(object) if is_list_or_tuple(object) else if_not_list_nor_tuple(object)


def to_single_if_one_item(list):
    """
        The opposite of to_list. Returns a single item if the give list has exactly on item. Otherwise returns a list
    :param list:
    :return:
    """
    return list[0] if len(list) == 1 else list


def map_item_or_items_or_dict_values(item_lambda, data):
    """
        Processes each item or the non-list single item with item_lambda and returns a list or single item accordingly
    :param item_lambda:
    :param data
    :return:
    """
    if (isinstance(data, dict)):
        # Map to a new dict. Pass through the keys and map the values
        return map_dict_to_dict(lambda key, value: [key, item_lambda(value)], data)
    else:
        # Map the item or list, return a single item or array
        return to_single_if_one_item(map(item_lambda, to_list(data)))


def is_iterable(object):
    return isinstance(object, collections.Iterable)


def to_dict_if_none(object):
    """
        Forces an object to be an empty dictionary if it is null
    """
    return {} if not object else object


def merge(*args):
    """
        Merges any number dictionaries together. The last duplicate dictionary keys always take precedence

        Keyword arguments:
            **args: any number of dictionaries
    """
    super_dictionary = {}
    for dictionary in args:
        super_dictionary = dict(super_dictionary.items() + dictionary.items())
    return super_dictionary

def deep_merge(*args):
    """
        Like merge but combines values that are both dicts by deep_merging them
    :param args:
    :return:
    """
    super_dictionary = {}
    for dictionary in args:

        matching_keys_of_dicts = filter(
            lambda key: type(super_dictionary[key]) == dict and type(dictionary[key] == dict),
            set(super_dictionary.keys()).intersection(set(dictionary.keys())))
        merged_dict = map_to_dict(lambda key: [key, deep_merge(super_dictionary[key], dictionary[key])], matching_keys_of_dicts)

        non_matching_keys = set(super_dictionary.keys()).union(set(dictionary.keys())).difference(matching_keys_of_dicts)
        super_dictionary = dict(
            filter(lambda tup: tup[0] in non_matching_keys, super_dictionary.items() + dictionary.items()) +
            merged_dict.items())
    return super_dictionary


def ordered_dict_merge(*args):
    """
        Merges any number dictionaries together. The last duplicate dictionary keys always take precedence

        Keyword arguments:
            **args: any number of dictionaries
    """
    super_dictionary = collections.OrderedDict()
    for dictionary in args:
        super_dictionary = collections.OrderedDict(super_dictionary.items() + dictionary.items())
    return super_dictionary


def filter_keys(dct, keys):
    """
        Remove all keys not given in keys from the dict, returning a copy with only the specified keys
    :param dict:
    :param keys:
    :return:
    """
    return dict((k, v) for k, v in dct.iteritems()
                if k in keys)


def remove_keys(dct, keys):
    """
        Remove the given keys from the dict, returning a copy of the dict with the keys removed
    :param dct:
    :param keys: Keys to match. If concatinated strings are used then recurse into the dictionaries to remove
    those. For instance 'foo.bar' removes bar keys in foo keyed dictionaries 'foo.*.bar' removes bar keys in
    any key under a foo key
    :return:
    """
    return dict((k,
                 # Recurs on v if it's a dict, only passing through matching keys
                 remove_keys(v, parse_key_strings(keys, k)) if isinstance(v, dict) else v)
                for k, v in dct.iteritems() if not k in keys)

def parse_key_strings(keys, segment):
    keys_segments = map(lambda key: key.split('.'), keys)
    return map(lambda key_segments: '.'.join(key_segments[1:]),
               filter(lambda key_segments: len(key_segments) > 1 and (key_segments[0] in ['*', segment]), keys_segments))

def remove_items(array, keys):
    """
        Remove the given keys from the dict, returning a copy of the dict with the keys removed
    :param array:
    :param keys:
    :return:
    """
    return filter(lambda item: item not in keys, array)


def dual_map(lambda_call, list1, list2):
    if len(list1) > len(list2):
        raise Exception('list1 has more elements than list2: {0} versus {1}'.format(list1, list2))
    return map(lambda index_and_val: lambda_call(index_and_val[1], list2[index_and_val[0]]),
               enumerate(list1))


def dual_map_to_dict(lambda_call, list1, list2):
    """
        Dual map two even length enumerables to key/value pairs
    :param lambda_call: Takes the first and second arguments as args and allows transformation of each, returning
    a two elemetn array to be the key and value
    :param list1:
    :param list2:
    :return: A dictionary
    """
    if len(list1) > len(list2):
        raise Exception('list1 has more elements than list2: {0} versus {1}'.format(list1, list2))
    return map_to_dict(
        lambda index_and_val: lambda_call(index_and_val[1], list2[index_and_val[0]]),
        enumerate(list1))


def map_dict(lambda_call, dict):
    """
        Maps the dict to key values.

        lambda_call takes each item and must returns a key and value as a tuple or list
    """
    return map(lambda tup: lambda_call(tup[0], tup[1]), dict.iteritems())

def compact_dict(dictionary):
    """
        Removes any key values of the dict that are null, returning a new dict
    :param dictionary
    :return:
    """
    results = {}
    for key, value in dictionary.iteritems():
        if value:
            results[key] = value
    return results

def map_to_dict(lambda_call, list):
    """
        Maps the list to key values.

        lambda_call takes each item and must returns a key and value as a tuple or list
    """
    results = {}
    for item in list:
        result_pair = lambda_call(item)
        results[result_pair[0]] = result_pair[1]
    return results


def map_dict_to_dict(lambda_call, dictionary):
    """
        Maps the list to key values.

        lambda_call takes each a key and value and must returns a key and value as a tuple or list
    """
    results = {}
    for key, value in dictionary.iteritems():
        result_pair = lambda_call(key, value)
        if result_pair:
            results[result_pair[0]] = result_pair[1]
    return results

def map_dict_value(lambda_call, dictionary):
    """
        Like map_dict_to_dict, but leaves the key alone and only maps the values
    :param lambda_call: A function expecting a value. If you need the key use map_dict_to_dict. Returns the mapped value
    :param dictionary:
    :return: A dictionary with the keys unchanged but values mapped
    """
    return map_dict_to_dict(lambda key, value: [key, lambda_call(value)], dictionary)

def map_to_keyed_collections(lambda_call, list):
    """
        Creates a dict keyed by the results of the lambda_call for each item and valued by the items themselves. items with the same key results are placed together in a selection
    :param lambda_call: Takes an item and returns the key to which it should map. Optionally return an object as the second return value. This will be used in place of the item for the dict value
    :param dictionary:
    :return:
    """
    result = {}
    for item in list:
        val = lambda_call(item)
        if is_list_or_tuple(val):
            key, obj = val
        else:
            key = val
            obj = item
        if not result.get(key, None):
            result[key] = []
        result[key].append(obj)
    return result


def flatten_values(dct):
    """
        Flattens the values of a dict containing arrays for values (the result of map_to_keyed_collections)
    :param dct:  e.g. {'a':[1,2,3],'b':[3,4,5]}
    :return: [1,2,3,3,4,5]
    """
    return flatten([v for k, v in dct.iteritems()])


def flat_map_values(lambda_call, dct):
    """
        Like flatten_values but also accepts a lambda which accepts each key and value and returns a collection result to be flattened. This is useful to make values of a particular key unique
    :param lambda_call:
    :param dct:
    :return:
    """
    return flatten([lambda_call(k, v) for k, v in dct.iteritems()])


def filter_dict(lambda_call, dictionary):
    """
        Filters a dictionary
    :param lambda_call: takes each kay and value and returns true to pass the set through the filter
    :param dictionary:
    :return:
    """
    return dict((key, value) for key, value in dictionary.iteritems() if lambda_call(key, value))


def get_value_of_first_matching_key(filter_lambda, dict, default):
    """
        Return the value of the first key that makes the filter_lambda return true, or else return the default. Since key order is arbitrary, you should only use this if one or no keys are expected to pass
    :param filter_lambda:
    :param dict:
    :param default:
    :return:
    """
    filtered_dict = filter_dict(filter_lambda, dict)
    return filtered_dict[filtered_dict.keys()[0]] if len(filtered_dict.keys()) > 0 else default


def map_to_2d_dict(outer_lambda, inner_lambda, list):
    """
        Create a 2D dictionary from the list
        outer_lambda should return a single item, the outer hash key
        inner_lambda should return a pair, the inner hash key and the value
    """
    results = {}
    for item in list:
        outer_key = outer_lambda(item)
        result_pair = inner_lambda(item)
        if not results.get(outer_key, False):
            results[outer_key] = {}
        results[outer_key].update({result_pair[0]: result_pair[1]})

    return results


def if_cond(value, predicate_lambda, map_lambda):
    """
        A simple wrapper to test a value with a predicate lambda and call a map lambda if the predicate is true
        value is the object to test
        predicate_lambda takes value and calls map_lambda if true or else returns value
        Returns value of the predicate returns false. Returns the map lambda result if the predicate returns true
    """
    if (predicate_lambda(value)):
        return map_lambda(value)
    return value


def if_cond_raise(value, predicate_lambda, exception_lambda):
    """
        Raises the exception returned by exception_lambda if predicate_lambda returns true. Both lambdas are passed value.
    """
    if (predicate_lambda(value)):
        raise exception_lambda(value)
    return value


def if_false_raise(predicate, exception_lambda):
    """
        Raises the exception returned by the exception_lambda if predicate is true.
    """
    if predicate:
        raise exception_lambda()


def first(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item):
            return item


def flatten(list_of_lists):
    """
        Shallow flatten a multi-dimensional list, meaning the top two dimensions are flattened and deeper ones are ignored
    """
    return list(chain.from_iterable(list_of_lists))


def flat_map(map_lambda, list):
    """
        Map a list to a list of lists and flatten the results
    """
    return flatten(map(map_lambda, list))

def flat_map_dict(map_dict_lambda, dct):
    """
        Maps a dict to a list per dict entry, then flattens those lists
    :param map_dict_lambda:
    :param dct:
    :return:
    """
    return flatten(map_dict(map_dict_lambda, dct))


def unique(seq, idfun=None):
# order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if (not marker in seen):
            seen[marker] = 1
            result.append(item)
    return result


def any_true(predicate_lambda, list):
    for item in list:
        if predicate_lambda(item):
            return True
    return False


def get_single_value_or_none(list):
    return list[0] if len(list) == 1 else None

def get_single_value_or_create(list, construct):
    """
        Returns the single value of the list if it has exactly one member or else calls the construct lambda
    :param list:
    :param construct:
    :return:
    """
    return list[0] if len(list) == 1 else construct()


def get_list_or_if_empty(list, default_lambda):
    """
        Returns teh given list if not-empty or calls the default_lambda and returns the results of it
    :param list:
    :param default_lambda:
    :return:
    """
    return list if len(list) > 0 else default_lambda()


class TooManyFoundException(Exception):
    pass


def one_or_none(list):
    """
        Raise an exception unless 0 or 1 results are in list
    :return: the single item or None
    """
    if len(list) > 1:
        raise TooManyFoundException("Expected 0 or 1 result but found {0}. Found: {1}".format(len(list), list))
    return list[0] if len(list) == 1 else None


def deep_copy_dict_structure(dct, convert_objects=False):
    """
        Traverse a dict, recreating the internal dict instances but leaving the non-dict values as identical references
    :param dct: The dict to deep copy
    :param convert_objects: Default False. Object instances are normally copied without altercation. If this is set to True then the __dict__ property will be used for the copy. This is removes the evidence of the class but is useful for converting to a simple dict/list/primitive structure
    :return:
    """
    return map_dict_to_dict(lambda key, value: [key, deep_copy(value, convert_objects)], dct)


def deep_copy_array_structure(array, convert_objects=False):
    return map(lambda value: deep_copy(value, convert_objects), array)


def deep_copy(value, convert_objects=False):
    if isinstance(value, dict):
        return deep_copy_dict_structure(value, convert_objects)
    elif is_list_or_tuple(value):
        return deep_copy_array_structure(value, convert_objects)
    elif convert_objects and hasattr(value, '__dict__'):
        # Attempt to handle objects
        return deep_copy_dict_structure(value.__dict__, convert_objects)
    else:
        # Primitives (or objects when convert_object==False)
        return value


def type_wrap(value, wrapper_lambdas):
    """
        Wraps the value using one of the wrapper_lambdas or returns value if no match is found
        :param value:
        :param wrapper_lambdas: dict of lambda wrappers, keyed by the type they should wrap. These wrappers can wrap all dict values and the outer dict. They can match the dict class itself or any other class. The wrapper will be looked up using wrapper_lambdas.get([type(value)], get_first(filter(lambda wrapper_key: isinstance(value, wrapper_key), wrapper_lambdas.keys()), deep_map_dict_structure(value)) so that if an exact match isn't found the keys will be searched for a parent class. If no match is found the value is returned as is
        :param the optional container of the value, for use by the lambda, which takes it as an optional second value
        :return:
    """
    # Try a direct key type match
    x = wrapper_lambdas.get(type(value),
                            # else lookup by inheritance.
                            get_value_of_first_matching_key(
                                lambda wrapper_key, wrapper_value: isinstance(value, wrapper_key),
                                wrapper_lambdas,
                                # else return value
                                lambda value: value))(value)
    return x


def deep_map_dict_structure(dcts_or_dct, wrapper_lambdas):
    """
        Deep maps a dct by recursively evaluating values and wrapper values based on type. Any value that is a dict will result in recursion on that value. The results of the recursion will wrapped with a wrapper_lambda keyed by type(dict) if one is specified. Thus dicts are always recursed on and returned as dicts, which can then be wrapped and transformed as needed. This includes the top level dict passed in.
    :param dcts_or_dct: one or more multi-level dicts. Pass a singular dict or array of dicts
    :param wrapper_lambdas: dict of lambda wrappers, keyed by the type they should wrap. These wrappers can wrap all dict values and the outer dict. They can match the dict class itself or any other class. The wrapper will be looked up using wrapper_lambdas.get([type(value)], get_first(filter(lambda wrapper_key: isinstance(value, wrapper_key), wrapper_lambdas.keys()), deep_map_dict_structure(value)) so that if an exact match isn't found the keys will be searched for a parent class. If no match is found the value is returned as is
    :return: If dcts is singular, a singular dict, otherwise an array of dicts
    """
    # Map the one or multiple items and return one or multiple items respectively
    return to_single_if_one_item(
        map(lambda dct_or_obj:
            # Map the dict to a transformed dict and type wrap, or if the value is not a dict, just type wrap it
            type_wrap(
                map_dict_to_dict(
                    lambda key, value:
                    # Either recurse on dicts or type_wrap non dicts and return them.
                    [key, deep_map_dict_structure(value, wrapper_lambdas)],
                    dct_or_obj) if isinstance(dct_or_obj, dict) else
                dct_or_obj,
                wrapper_lambdas),
            to_list(dcts_or_dct)))


def resolve_property(obj, property):
    """
        Resolves a property string of an instance as a simple attribute or a simple getter if the property represents a no-arg method
    :param obj:
    :param property:
    :return:
    """
    value = getattr(obj, property)
    return value() if isfunction(value) else value


def map_property(dicts_or_objs, property):
    """
        Map the list of dicts or objects to property specified by the property string. attr() will be used to resolve object properties,
        and any property that represents a simple getter will be called as a no-arg function
    :param list_of_dicts_or_objs:
    :param property: a string representing the attribute or dict key
    :return: The values of the property for each list or dict
    """
    return map(lambda dict_or_obj:
               dict_or_obj[property] if isinstance(dict_or_obj, dict) else resolve_property(dict_or_obj, property),
               dicts_or_objs)


def get_first(list, default):
    """
        Return the first result of the list or the default if the list is empty
    :param list:  non-null list
    :param default:
    :return:
    """
    return (list[:1] or [default])[0]

def get_first_map(map_lambda, list):
    """
        Returns the first mapped item that isn't null
    :param map_lambda:
    :param list:
    :return:
    """
    for item in list:
        result = map_lambda(item)
        if result:
            return result

def if_not_none(obj, do_lambda):
    """
        Call the lambda with the given obj if the object is not none. Else return None
    :param obj:
    :param do_lambda:
    :return:
    """
    return do_lambda(obj) if obj else None


def accumulate(accumulate_lambda, target, list):
    """
        TODO this exists in python 3
        A type of aggregate function that begins with a target and a list of items that are mapped to chainable functions
        of the target. The first mapped item of list is called on target and then subsequent mapped items are called on the
        result of the previous call,
    :param map_lambda: Takes the current mapped item of the list as arguments. Returns the next target
    :param target: The target object of the first mapped item of list. The result of called the mapped item on the target is the target used
     for the next item of the list
    :param list:
    :return:
    """
    if len(list) > 0:
        return accumulate(accumulate_lambda, accumulate_lambda(target, list[0]), list[1:])
    else:
        return target

def all_existing_classes_subclass(dct_or_obj, **kwargs):
    """
        Checks that all the values in kwargs are classes that subclass/equal the corresponding key value in
        dct_or_obj. If dct_or_obj doesn't have one of the keys, that key is ignored.
    :param dct_or_obj:
    :param kwargs:
    :return: True if all match
    """
    for key, sub_class in kwargs.items():
        base_class = dct_or_obj.get(key, None) if isinstance(dct_or_obj, dict) else getattr(dct_or_obj, key)
        if sub_class and base_class and not issubclass(sub_class, base_class):
            return False
    return True

def all_existing_keys_match(dct_or_obj, **kwargs):
    """
        Checks that all the key values in matching_dict are values that equal the corresponding key in
        dct_or_obj. If either has a null value for the key, it is ignored
    :param dct_or_obj:
    :param kwargs:
    :return: True if all match
    """
    for key, value in kwargs.items():
        matching_value = dct_or_obj.get(key, None) if isinstance(dct_or_obj, dict) else getattr(dct_or_obj, key)
        if value and matching_value and  matching_value != value:
            return False
    return True

