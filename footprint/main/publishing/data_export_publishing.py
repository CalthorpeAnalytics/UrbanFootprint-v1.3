import logging
import os
import shlex
import shutil
import traceback

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.utils import timezone

from sendfile import sendfile
import sys
from tastypie.models import ApiKey
from footprint.celery import app
from footprint.common.utils.async import start_and_track_task
from footprint.common.utils.websockets import send_message_to_client
from footprint.common.utils.zip_geodatabase import zip_file_gdb


from footprint.main.models.keys.keys import Keys
from footprint.main.models.presentation.layer import Layer
from footprint.main.models.tasks.async_job import Job
from footprint.main.utils.utils import timestamp, database_connection_string_for_ogr
from footprint import settings

__author__ = 'calthorpe_associates'
logger = logging.getLogger(__name__)


SUPPORTED_FORMATS = {
    "geojson": '''"GeoJSON"''',
    "gdb": '''"FileGDB"''',
    "shapefile": '''"ESRI Shapefile"'''
}


def export_layer(request, layer_id, api_key):
    job = start_and_track_task(_export_layer, api_key, layer_id)
    return HttpResponse(job.hashid)


@app.task
def _export_layer(job, layer_id):

    try:
        layer = Layer.objects.get(id=layer_id)
        job.status = "Exporting"
        job.save()

        db_entity = layer.db_entity_interest.db_entity

        export_file, filename = export_db_entity_to_file(db_entity)

        job.status = "Zipping"
        job.save()

        zip_file_gdb(export_file)
        shutil.rmtree(export_file)

        job.data = '/' + filename + ".zip"
        job.save()

        send_message_to_client(job.user.id, dict(event='layerExportCompleted',
                                                 layer_id=layer_id,
                                                 job_id=str(job.hashid)))

        job.status = 'Complete'

    except Exception, e:
        job.status = "Failed"

        exc_type, exc_value, exc_traceback = sys.exc_info()
        readable_exception = traceback.format_exception(exc_type, exc_value, exc_traceback)
        job.data = readable_exception
        job.save()

        send_message_to_client(job.user.id, dict(event=job.type + " failed", trace=readable_exception))

    print job.status, job.data
    job.ended_on = timezone.now()
    job.save()
#
#     return tracked_job
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
    print "trying to send " + filepath
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

    print "attempting to create" + export_file

    export_command = generate_ogr_command(export_format, select_statement, export_file)
    export_command_args = shlex.split(export_command)
    print export_command, export_command_args
    # shlex ("simple lexical analysis") splits the command string into its arguments before it runs in subprocess
    ogr_result = os.system(export_command) #, shell=True)
    # print result
    if ogr_result:
        raise Exception(ogr_result)
    logger.info("file ready for download")

    return export_file, filename


def generate_ogr_command(export_format, select_statement, export_file):
    ogr_command = "/usr/local/bin/ogr2ogr -append -f {ogr_format} -sql \'{select_statement}\' -nlt MULTIPOLYGON {export_file} "\
        "PG:\"{db_connection}\" {options}"
    logger.debug("Data Export: " + ogr_command)

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



