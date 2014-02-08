import os
from inspect import getmro

from footprint.initialization.publishing.layer_initialization import LayerMediumKey
from footprint.lib.functions import map_to_dict
from footprint.models.presentation.template import Template
from footprint.models.keys.keys import Keys
from settings import FOOTPRINT_TEMPLATE_DIR


__author__ = 'calthorpe'


def create_template_context_dict_for_parent_model(parent_model, color_resolver):
    """
        Creates the context_dict for the given model by iterating through all of its child instances and styling
        its parent foreign_key (e.g. BuiltForm subclasses' parent foreign key is built_form_id)
    :param parent_model: The model that has a parent foreign key
    :param color_resolver: A function that accepts the instance as an argument and returns the correct color.
    :return: A complete default context_dict for all instances of the give model
    """
    parent_foreign_key = '%s_%s' % (parent_model._meta.module_name, parent_model._meta.pk.attname)
    context_dict = null_context_dict([parent_foreign_key])
    try:
        all = list(parent_model.objects.all())
    except Exception:
        from django.db import connection
        connection._rollback()
        all = list(parent_model.objects.all())

    for instance in all:
        color = color_resolver(instance)
        if color:
            try:
                context_dict['attributes'][parent_foreign_key]['equals'][instance.id] = color_resolver(instance)
            except KeyError, e:
                raise Exception("KeyError for context_dict['attributes']['%s']['equals'][%s]. Original Exception: %s" % (parent_foreign_key, instance.id, e.message))

    return context_dict


def create_template_context_dict_for_foreign_key(foreign_key_model_field, color_lookup, color_lookup_field):
    """
        Creates the CSS context_dict to use in a TemplateContext instance for the given ForeignKey model field
    :param foreign_key_model_field: A Django models.ForeignKey which will be styled to a color
    :param color_lookup: A dict that maps a field of the ForeignKey model class to a color
    :param color_lookup_field: The field of the ForeignKey model that matches the keys of the color_lookup
    :return: A complete default context_dict for the give model field
    """

    foreign_model = foreign_key_model_field.rel.to
    foreign_key_attribute_name = foreign_key_model_field.attname

    template_context_dict = null_context_dict([foreign_key_attribute_name])

    for lookup_field_value, color in color_lookup.iteritems():
        if not color:
            continue
        try:
            foreign_key = foreign_model.objects.get(**{color_lookup_field: lookup_field_value}).id
        except:
            continue

        template_context_dict['attributes'][foreign_key_attribute_name]['equals'][foreign_key] = {
            'fill': {'color': color},
        }

    return template_context_dict


def null_context_dict(styled_attributes):
    """
        For the given attributes strings, returns a context_dict with only null selectors. This is the starting point
        for building a context_dict. The null fill and color are hard-coded.
    :param styled_attributes:
    :return: an incomplete context_dict to be filled out by other functions
    """
    return {
        'htmlClass': None,
        'attributes': map_to_dict(lambda styled_attribute: [
            styled_attribute,
            {
                'equals': {
                    'null': {
                        "fill": {
                            "color": '#f8fcff',
                            "opacity": .2
                        },
                        "outline": {
                            "color": "#FFFFFF"
                        }
                    },
                },
                'greater_than': {},
                'less_than': {}
            }
        ],
                                  styled_attributes),
    }


def load_style_templates(styled_class, styled_attribute=None):
    """
        Looks for a style template based on the styled_class and styled_attribute. The latter is optional. If no
        file exists for the combination, the code will search for the nonattributed style. If that fails, the code
        will continue the search with each ancestor of the styled_class, with and without attribute, until a match is
        found.
    :param styled_class: The class that represents the table being styled
    :param styled_attribute: Optional. The attribute being styled.
    :return:
    """
    for cls in getmro(styled_class):
        if styled_attribute:
            attributed_cartocss_file = FOOTPRINT_TEMPLATE_DIR + "/maps/%s__%s.cartocss" % (cls.__name__, styled_attribute)
            nonattributed_cartocss_file = attributed_cartocss_file.split('__')[0]+'.cartocss'
        else:
            attributed_cartocss_file = None
            nonattributed_cartocss_file = FOOTPRINT_TEMPLATE_DIR + "/maps/%s.cartocss" % cls.__name__

        for cartocss_file in map(lambda f: f, [attributed_cartocss_file, nonattributed_cartocss_file]):
            if os.path.exists(cartocss_file):
                cartocss_style_template = open(
                    cartocss_file,
                    "r").read()

                css_file = cartocss_file.replace('.cartocss', '.css')
                standardcss_style_template = open(
                    css_file, "r").read()
                return dict(cartocss=cartocss_style_template, css=standardcss_style_template)
    raise Exception("No style file found for style_class %s (nor its ancestors) %s %s without styled_attribute %s" %
                    (styled_class.__name__,
                     ', '.join(map(lambda cls: cls.__name__, getmro(styled_class))),
                     'neither with nor' if styled_attribute else '',
                     styled_attribute or ''))


def create_style_template(template_context_dict, db_entity_key, styled_class=None, *styled_attributes):
    """
        Creates a TemplateContext and Template that contains that TemplateContext for CSS styling.
    :param template_context_dict: A python dict which reveals what key values can be set by the user to be
    used as the context of the CSS Django templates. The dict should have default values.
    :param db_entity_key. The db_entity_key that the layer represents. This is used to name the template_key
        if the styled_class isn't specified
    :param styled_class. The optional feature class upon which the template key is named. If this is omitted,
    a generic template is created that doesn't load any predefined style info from the system.
        TODO There is no particular purpose for a Template based on only a db_entity_key at this point.
        The one based on a styled_class (Feature class) can load the template matching the class and attributes to
        provide default styling for the layer. We might have a case for having various generic default styling for a
        layer that is not based on a feature_class.:w
    :return:
    """

    # Construct a template to use for Layer instances that show a geographic selection
    template_key = LayerMediumKey.Fab.ricate(styled_class.__name__ if styled_class else db_entity_key)
    Template.objects.update_or_create(
        key=template_key,
        defaults={
            'name': template_key,
            'content_type': Keys.CONTENT_TYPE_CSS,
            'content': dict(
                # Creates a dict(attribute1:dict(cartocss:a_cartocss_template, css:a_regular_css_template), ...)
                attributes=map_to_dict(
                    lambda styled_attribute:
                        [styled_attribute, load_style_templates(styled_class, styled_attribute)],
                    styled_attributes)
            ),
            'template_context': template_context_dict,
            'description': 'The tilestache CSS template for class %s' % styled_class.__name__
        })