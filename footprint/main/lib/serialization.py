from django.core import serializers
from django.core.serializers import json
from footprint.main.lib.functions import merge, remove_keys, is_list_tuple_or_dict

__author__ = 'calthorpe_associates'

def json_serialize(objects):
    """
        Serializes by removing the fields property from serialization in favor of a flatter dictionary
    """
    # this gives you a list of dicts
    raw_data = serializers.serialize('python', objects)
    # now extract the inner `fields` dicts
    actual_data = cond_deep_flat_map_iterable(raw_data)
    # and now dump to JSON
    return json.dumps(actual_data)

def cond_deep_flat_map_iterable(iterable):
    if (type(iterable) == dict):
        # Flatten the dictionary of the fields key if it exists
        flattened_dict = remove_keys(
            merge(iterable, iterable.get('fields', {})),
            ['fields']
        )
        # Map each key value, recursing into the value if it's a dict or iterable
        return dict([(key, cond_deep_flat_map_iterable(value) if is_list_tuple_or_dict(value) else value)
            for key, value in flattened_dict.iteritems()])
    else:
        return map(lambda item: cond_deep_flat_map_iterable(item) if is_list_tuple_or_dict(item) else item, iterable)

def json_deserialize(json):
    return json.loads(json, to_raw_data)

def to_raw_data(dct):
    model = dct['model']
    pk = dct['pk']
    raw_data = { }
    raw_data['model'] = model
    raw_data['pk'] = pk
    raw_data['fields'] = to_raw_data(remove_keys(dict, ['model', 'pk']))
    return raw_data


