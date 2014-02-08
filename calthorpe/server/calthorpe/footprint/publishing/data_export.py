import logging
import os
import shlex
import shutil
import subprocess
from celery.task import task
import datetime
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from django.utils import timezone
from sendfile import sendfile
from tastypie.models import ApiKey
from common.utils.websockets import send_message_to_client
from common.utils.zip_geodatabase import zip_file_gdb
from footprint.models import Scenario
from footprint.models.keys.keys import Keys
from footprint.models.presentation.layer import Layer
from footprint.models.tasks.async_job import Job
from footprint.utils.utils import timestamp, database_connection_string_for_ogr
import settings

__author__ = 'calthorpe'
logger = logging.getLogger(__name__)


SUPPORTED_FORMATS = {
    "geojson": '''"GeoJSON"''',
    "gdb": '''"FileGDB"''',
    "shapefile": '''"ESRI Shapefile"'''
}


def handle_export_request():
    pass


def export_scenario(request, scenario_id, export_format="gdb", fields=None):
    _export_scenario(scenario_id, export_format, fields)


@task
def _export_scenario(scenario_id, export_format="gdb", fields=None):
    scenario = Scenario.objects.get(id=scenario_id)

    export_filename = construct_export_filename(scenario, export_format)

    scenario_layer_keys = [Keys.DB_ABSTRACT_FUTURE_SCENARIO_FEATURE,
                          Keys.DB_ABSTRACT_INCREMENT_FEATURE,
                          Keys.DB_ABSTRACT_END_STATE_FEATURE]

    db_entities = [interest.db_entity for interest in scenario.dbentityinterest_set.filter(db_entity__key__in=scenario_layer_keys)]
    for db_entity in db_entities:
        export_file, filename = export_db_entity_to_file(db_entity,
                                                         export_file=os.path.join(settings.STATIC_ROOT,export_filename))

    zip_file_gdb(export_file)
    os.remove(export_file)
    download_path = settings.STATIC_URL + export_filename + ".zip"
    return HttpResponse(download_path)


def export_layer(request, layer_id, api_key):
    user_id = ApiKey.objects.get(key=api_key).user_id
    job = Job.objects.create(
        type="export layer",
        status="New",
        user=User.objects.get(id=user_id)
    )
    job.save()

    task = _export_layer.apply_async(
        args=[job.hashid, layer_id, user_id],
        soft_time_limit=3600,
        time_limit=3600,
        countdown=1
    )

    job = Job.objects.get(hashid=job.hashid)
    job.task_id = task.id
    job.save()

    return HttpResponse(job.hashid)


@task
def _export_layer(hash_id, layer_id, user_id):
    layer = Layer.objects.get(id=layer_id)
    job = Job.objects.get(hashid=hash_id)
    job.status = "Exporting"
    job.save()
    try:
        db_entity = layer.db_entity_interest.db_entity

        export_file, filename = export_db_entity_to_file(db_entity)

        job.status = "Zipping"
        job.save()

        zip_file_gdb(export_file)
        shutil.rmtree(export_file)

        job.data = "/" + filename + ".zip"
        job.status = "Complete"
        job.save()

        send_message_to_client(user_id,
                           dict(event='export_complete',
                                job_id=job.hashid))

    except Exception, E:
        job.status = "Failed"
        job.data = E
        job.save()
        send_message_to_client(user_id, dict(event='export_failed'))

    job.ended_on = timezone.now()
    job.save()


def get_export_result(request, api_key, hash_id):
    job = Job.objects.get(hashid=hash_id)

    try:
        user_id = ApiKey.objects.get(key=api_key).user_id
        assert user_id == job.user.id
    except:
        return HttpResponseForbidden("This user did not request that file!")

    if job.status != "Complete":
        return HttpResponseNotFound("Export is not complete")

    filepath = settings.SENDFILE_ROOT + job.data
    return sendfile(request, filepath)


def export_db_entity_to_file(db_entity, export_file=None, export_format="gdb", fields=None):

    if fields:
        field_string = ''
        for field in fields:
            field_string += field + ', '
        field_string = field_string[:-2]
    else:
        field_string = " * "

    table = "{schema}.{table}".format(**db_entity.__dict__)

    select_statement = "select * from (select {fields} from {table}) as {feature_class};".format(
        fields=field_string, table=table, feature_class=db_entity.key)
    filename = construct_export_filename(db_entity, export_format)

    if not export_file:
        export_file = "{SENDFILE_ROOT}/{filename}".format(
            SENDFILE_ROOT=settings.SENDFILE_ROOT,
            filename=filename)

    print export_file

    export_command = generate_ogr_command(export_format, select_statement, export_file)

    # shlex ("simple lexical analysis") splits the command string into its arguments before it runs in subprocess
    subprocess.call(shlex.split(export_command))
    logger.info("file ready for download")

    return export_file, filename


def generate_ogr_command(export_format, select_statement, export_file):
    ogr_command = "ogr2ogr -append -f {ogr_format} -sql \'{select_statement}\' -nlt MULTIPOLYGON {export_file} "\
        "PG:\"{db_connection}\" {options}"

    options = "FGDB_BULK_LOAD" if export_format == 'gdb' else ''

    return ogr_command.format(
        ogr_format=SUPPORTED_FORMATS[export_format],
        srs=Keys.SRS_4326,
        select_statement=select_statement,
        export_file=export_file,
        db_connection=database_connection_string_for_ogr('default'),
        options=options
    )


def construct_export_filename(entity, extension):
    export_file_name = "{db_entity}_{timestamp}.{extension}".format(
        db_entity=entity.name.replace(" ", "_"),
        timestamp=timestamp(),
        extension=extension)

    return export_file_name



