import os
import shutil
from django.contrib.auth.models import User
from footprint.main.models.database.information_schema import verify_srid
from django.conf import settings
from footprint.main.publishing.shapefile_processor import unpack_shapefile, import_shapefile_to_db

__author__ = 'calthorpe_associates'

sample_data_path = os.path.join('srv', 'calthorpe', 'urbanfootprint', 'footprint', 'main', 'samples')

test_shps = [
    dict(
        zip_path=os.path.join(sample_data_path, 'ZipCodes2009.zip'),
        srid=102642,
        new_name='test_zipcodes',
        user=User.objects.get(username='test')
    ),
    dict(
        zip_path=os.path.join(sample_data_path, 'TAZ07_w_tahoe.zip'),
        srid=102642,
        new_name='test_taz',
        user=User.objects.get(username='test')
    )
]

def test_shp_uploads():
    for shp in test_shps:
        load_test_shp(**shp)

def load_test_shp(zip_path="/srv/calthorpe/urbanfootprint/footprint/main/samples/ZipCodes2009.zip",
                  srid=102642,
                  new_name='my_zipcodes',
                  user=User.objects.get(username='test')):
    spatial_ref = verify_srid(srid)
    shutil.copy(zip_path, settings.MEDIA_ROOT)
    shapefile_zip = os.path.join(settings.MEDIA_ROOT, os.path.basename(zip_path))

    shp, files_to_import = unpack_shapefile(shapefile_zip, 'zipcodes', user)
    shp = os.path.join(settings.MEDIA_ROOT, shp)
    import_shapefile_to_db(shp, new_name, spatial_ref)