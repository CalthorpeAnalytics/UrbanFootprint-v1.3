__author__ = 'calthorpe'

from django import forms
from django.forms import ModelForm, Form
from django.forms.models import ModelChoiceField, ValidationError
from django.db.models import FileField
#
#

from datetime import datetime
from calthorpe import footprint
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.simple import direct_to_template
from django.core.files import File
import os, zipfile
from calthorpe.footprint.forms import UploadGeometryForm
from calthorpe.footprint.uf_tools import executeSQL_now
from calthorpe.settings import SHAPEFILE_TYPES, USER_GEOM_LIBRARY, MEDIA_ROOT

# TODO: integrate these imports with the new model structure
from footprint.models.scenario import Scenario
from footprint.models.study_area import StudyArea
from footprint.models.layer_style import LayerStyle
from footprint.models.geo_layer import GeoLayer
from footprint.models.study_area_geo_layer import StudyAreaGeoLayer
from geoserver_utils import sync_layer_with_geoserver


class UploadGeometryForm(forms.Form):
    def validate_file_extension(value):
        if not value.name.endswith('.zip'):
            raise ValidationError(u'Upload works only for ShapeFiles (.shp)')
    shp = forms.FileField(required=False, validators=[validate_file_extension])
    name_for_table = forms.CharField()
    SRID = forms.IntegerField(required=False)


def handle_uploaded_shp(request, scenario_id):
    '''
    Handles a zipped shapefile folder, uploads the geometry to the project DB, adds the data to a
    geo_layer, and styles that layer for the current study area.
    '''

    # read and process geometry form
    geom_form = UploadGeometryForm(request.POST, request.FILES)
    if geom_form.is_valid():
        name = geom_form.cleaned_data['name_for_table']
        srid = geom_form.cleaned_data['SRID']
        zip = geom_form.cleaned_data['shp']
    else:
        return "Could not process the form..."
    try:
        upload_process = upload_shp(zip, name)
        shp = upload_process[0]
        archive_contents = upload_process[1]
    except Exception, E:
        print E
        raise

    import_shapefile_to_db(shp, srid, name, scenario_id)
    add_uploaded_geom_to_map(scenario_id, name, shp[:-4])
    # remove uploaded shapefile objects
    for file in archive_contents:
        os.remove(os.path.join(MEDIA_ROOT, file))
    #    if ret > 1:
    #        context['msg'] = 'Error processing Shapefile: ' +  ret
    #        return render_to_response('/footprint/error.html', context , context_instance = RequestContext(request) )
    return 'Loaded New Shapefile succesfully'

def upload_shp(zip, user_defined_name):
    archive = zipfile.ZipFile(zip, 'r')
    archive_contents = archive.namelist()
    only_shp = None
    # verify that each file in the archive corresponds with a known shapefile type and is not
    # named with any strings that may compromise our servers
    for a in archive_contents:
        for type in SHAPEFILE_TYPES:
            if a.endswith(type) and not a.startswith('/') and not ('..') in a:
                only_shp = True

    # if the files seem okay, extract them to the media root
    if only_shp:
        try: archive.extractall(path=MEDIA_ROOT)

        except Exception, E:
            for file in archive_contents:
                try: os.remove(os.path.join(MEDIA_ROOT, file))
                except: pass
            print E
            raise
    # if they look dangerous, or don't conform to our expectations, reject them
    else:
        msg =  'Uploaded ZIP contains non-shapefile data -- please try uploading a ZIP with only'\
               'a shapefile and its associated content'
        return msg
        # rename shp files to the user specified table name, so that the table is created with the proper name
    files_to_import = []
    for a in archive_contents:
        # TODO: validate user-supplied name to make sure it isn't hacky
        rename = "mv {0}/{1} {0}/{2}".format(MEDIA_ROOT, a, user_defined_name + a[-4:])
        os.system(rename)
        b = a.replace(a[:-4], user_defined_name)
        if a.endswith('.shp'):
            shp = b
        files_to_import.append(b)

    return shp, files_to_import

def import_shapefile_to_db(shp, user_defined_name, scenario_id, srid=None):
    # Take an unzipped shapefile through a form and bring the data into public schema, rename it, move it to a more
    # appropriate place, and index it

    # TODO: look for SRID in the shapefile contents
    # TODO: only use 'srid' arg if there is no .prj
    # TODO: throw exception if there is neither 'srid' arg nor .prj

    scenario = Scenario.objects.filter(id=scenario_id)[0]
    db = scenario.get_db()
    get_srid = ''' select srtext from spatial_ref_sys where srid = {0}'''.format(srid)
    using_srid = executeSQL_now(scenario.study_area.inputs_outputs_db, [get_srid])

    import_to_db = '''shp2pgsql -s {4}:3857 -g wkb_geometry -I {0} | psql -h {1} -U {2} -d {3} -q
    '''.format(os.path.join(MEDIA_ROOT, shp), db['HOST'], db['USER'], db['NAME'], srid)
    os.system(import_to_db)
    table_name = shp[:-4]

    #    rename = '''alter table "{0}" rename to {1};
    #                alter table {1} drop constraint "{0}_pkey";
    #                alter table {1} add primary key (gid);
    #                alter sequence "{0}_gid_seq" rename to "{1}_gid_seq"'''.format(table_name, user_defined_name)
    move_to_user_library = '''alter table {0} set schema {1};
                             '''.format(user_defined_name, USER_GEOM_LIBRARY)
    #    convert_to_wkb = '''--alter table {0}.{1} add column wkb_geometry geometry;
    #                        --update {0}.{1} set wkb_geometry = AsBinary(the_geom);
    #                        --alter table {0}.{1} drop column the_geom cascade;
    #                        --update {0}.{1} set wkb_geometry =  st_setSRID(wkb_geometry, {2});'''.format(USER_GEOM_LIBRARY, user_defined_name, srid)
#
#        reproject = '''update {0}.{1} set wkb_geometry = st_transform(wkb_geometry, 900913);
#            update {0}.{1} set wkb_geometry = st_setSRID(wkb_geometry, 900913);'''.format(USER_GEOM_LIBRARY, user_defined_name)
#        spatial_index = '''create index {0}_geom_idx on {1}.{0} using GIST (wkb_geometry);'''.format(user_defined_name, USER_GEOM_LIBRARY)

    executeSQL_now(scenario.study_area.inputs_outputs_db, [move_to_user_library]) #, rename, convert_to_wkb, reproject, spatial_index])

def add_uploaded_geom_to_map(scenario_id, name, original_name):

#    TODO: integrate this part with our user auth code
    try: user = user.id
    except: user = "[user]"

    # TODO: make sure there is a default style to use, and if not, create one.
    if not LayerStyle.objects.filter(name="uploaded_default"): pass
    else: pass
    
    style = LayerStyle.objects.filter(name="uploaded_default")[0]

    # publish layer to geoserver
    sync_layer_with_geoserver(USER_GEOM_LIBRARY, name, None)

    # layer to geo_layers
    new_geo_layer = GeoLayer()
    new_geo_layer.name = new_geo_layer.table_name = name

    new_geo_layer.description = "geometry uploaded by {0} from {1} on {2}".format(user, original_name, datetime.now())
    new_geo_layer.save()

    # add geo_layer to study_area_geo_layer
    scenario = Scenario.objects.filter(id=scenario_id)[0]
    study_area_layer = StudyAreaGeoLayer()
    study_area_layer.study_area = scenario.study_area
    study_area_layer.geo_layer = new_geo_layer
    study_area_layer.layer_style = style
    study_area_layer.save()
