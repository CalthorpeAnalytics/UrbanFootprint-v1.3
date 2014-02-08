import shlex
import subprocess
import json

from django.template import Template, Context

from footprint.models.keys.keys import Keys
from footprint.utils.utils import database_settings, create_static_content_subdir
from settings import MEDIA_ROOT


__author__ = 'calthorpe'


def render_attribute_styles(layer):
    """
        Iterates through the Layer.medium_context attributes, using the context stored for each attribute to render
        the css and cartocss style templates. The results are placed in the layer.rendered_medium in the form
        dict(attribute1:dict('css':rendered_css, 'cartocss': rendered_carto_css)). The carto_css is actually a file
        path since this is required by tilestache (TODO that it can't be a string)
    :param layer:
    :return:
    """

    # Fetch the dictionary of styles data for each styled attribute
    style = layer.medium_context
    style['id'] = layer.name

    # Write the style to the filesystem
    for attribute, attribute_context in layer.medium_context['attributes'].items():
        layer.rendered_medium[attribute] = {}
        layer.rendered_medium[attribute]['css'] = make_css(layer, attribute)
        layer.rendered_medium[attribute]['cartocss'] = make_carto_css(layer, attribute)

    layer.save()

    return layer


def make_css(layer, attribute):
    """
        Loads the SVG CSS for the given attribute name
    :param layer: The Layer instance
    :param attribute: An attribute/column of the DbEntity, such as built_form_id
    :return:
    """

    # Take the possibly customized context of the layer. If the dict has not been customized, it will simply
    # match the default default layer.medium.template_context.context
    customized_context = Context(layer.medium_context)
    formatted_style = Template(layer.medium.content['attributes'][attribute]['css']).render(customized_context)
    return formatted_style


def make_carto_css(layer, attribute):
    """
    Renders a mapnik XML file based on the properties of the layer and, optionally,
    style attributes. This process first writes an MML file to the filesystem. It then invokes the node.js
    carto command to create a carto xml file

    :param layer:
    :param attribute:
    :return:
    """
    mml = make_mml(layer, attribute)
    xml_filepath = carto_css(mml, layer.name)
    return xml_filepath


def make_mml(layer, attribute):
    """
    Generates mml string from a layer and a style
    :param layer: Layer object
    :param attribute: the attribute of the layer object that is getting styled

    :return:
    """
    carto_css_style = make_carto_css_style(layer, attribute)
    #sys.stdout.write(str(carto_css_style))
    db = database_settings(layer.presentation.config_entity.db)
    db_entity = layer.db_entity_interest.db_entity
    table = "{0}.{1}".format(db_entity.schema, db_entity.table)
    mml = {
        "Layer": [
            {
                "Datasource": {
                    "dbname": db['NAME'],
                    "extent": "",
                    "geometry_field": "wkb_geometry",
                    "host": "localhost",
                    "password": db['PASSWORD'],
                    "port": db['PORT'],
                    "srid": 4326,
                    "table": table,
                    "type": "postgis",
                    "user": db['USER'],
                },
                "id": layer.id,
                "name": layer.name,

                #TODO: look up layer tag from the library so that we can use this function for any layer
                # (and not just canvases)
                "class": db_entity.key,

                #TODO: look up geometry type from the geometry_columns table
                "geometry": "polygon",
                "srs": Keys.SRS_4326,
            },
        ],
        "Stylesheet": [carto_css_style],
        "interactivity": True,
        "maxzoom": 15,
        "minzoom": 7,
        "format": "png",
        "srs": Keys.SRS_GOOGLE,

    }
    #sys.stdout.write(str(mml))
    return json.dumps(mml)


def make_carto_css_style(layer, attribute):
    """
    :param layer: the layer to be styled
    :param attribute: The attribute whose cartocss template is to be rendered with the layer.medium_context as the
    template context
    :return  dict with an id in the form {layer.name}.mss and data key valued by the rendered template
    """

    style_template = Template(layer.medium.content['attributes'][attribute]['cartocss'])
    context = Context(layer.medium_context)
    formatted_style = style_template.render(context)
    return {
        'id': '{0}.mss'.format(layer.name),
        'data': "{0}".format(formatted_style)
    }


def carto_css(mml, name):
    """
    Takes MML string input and writes it to a Mapnik XML file.
    :param mml: an mml string, containing the proper CartoCSS styling and connection attributes required by the
    CartoCSS conversion program
    :param name: the unique name of the layer (standard method is to name it with its database schema and table name)
    :return mapfile: a cascadenik-ready document.
    """

    create_static_content_subdir('cartocss')
    mmlFile = "{0}/cartocss/{1}.mml".format(MEDIA_ROOT, name)
    mapFile = mmlFile.replace(".mml", ".xml")
    f = open(mmlFile, 'w+')
    f.write(mml)
    f.close()

    carto_css_command = shlex.split("carto -l {0} > {1}".format(mmlFile, mapFile))
    try:
        carto_css_content = subprocess.check_output(carto_css_command)
        f = open(mapFile, 'w')
        f.write(carto_css_content)
        f.close()

    except Exception, e:
        print "failed to generate cartocss for {mml}. fix the mml and run footprint_init --tilestache --skip"
        f = open(mmlFile, 'r')
        file_contents = f.read()
        f.close()
        #raise Exception("could not generate Mapnik XML: {0} {1}".format(e.message, file_contents))

    return mapFile

