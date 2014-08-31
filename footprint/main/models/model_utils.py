from footprint.main.lib.functions import map_to_dict

__author__ = 'calthorpe'

def model_field_names(model):
    opts = model._meta
    return map(lambda field: field.name, opts.fields + opts.many_to_many)

def field_value(model_instance, field, include_null=False):
    """
        Returns a tuple of the field name and model_instance value of that field if not null, otherwise
        returns null unless include_null=True
    """
    try:
        value = getattr(model_instance, field.name)
        return [field.name, value] if include_null or value else None
    except:
        # Proabably a toOne that isn't accessible yet
        return None

def model_dict(model_instance, include_null=False, include_many=False, omit_fields=[]):
    """
        Returns a dict keyed by field name and valued by model_instance's corresponding field value
        Primary keys are not included
        :param model_instance: The model instance
        :param include_null: Default False, set True to return fields that evalate to null
        :param omit_fields: Default [], list fields to omit. This is good if there are fields that throw an
        error if null or are simply unwanted
    """

    if not model_instance:
        return dict()

    opts = model_instance.__class__._meta
    return map_to_dict(lambda field: field_value(model_instance, field, include_null),
                       filter(lambda field: not field.primary_key and field.name not in omit_fields,
                              opts.fields + (opts.many_to_many if include_many else [])
                       )
    )

# UrbanFootprint class path builder
def uf_model(model_path):
    return 'footprint.main.models.%s' % model_path

def form_module_name(module, module_fragment, schema):
    return '%s.%s.%s_%s' % (schema, module, schema, module_fragment) if module else \
        '%s.%s_%s' % (schema, schema, module_fragment)

