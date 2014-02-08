#!/bin/bash -e

if [[ $FORCE_DELETE_VIRTUALENV = true ]]; then
  rm -rf $WORKSPACE/calthorpe_ve
fi

cd $WORKSPACE
virtualenv -q calthorpe_ve
source $WORKSPACE/calthorpe_ve/bin/activate

#workaround for stupid GDAL python binding bug
# EDIT -- this is failing every time the thing runs - commenting it until I talk to Ragi (EB)
# if [ $FORCE_DELETE_VIRTUALENV = true ]; then
#  pip install --no-install GDAL
#  cd $WORKSPACE/calthorpe_ve/build/GDAL
#  python setup.py build_ext --include-dirs=/usr/include/gdal/
#  pip install --no-download GDAL
# fi

cd $WORKSPACE/calthorpe/server/calthorpe

pip install -r pip-req.txt
if [ ! -f local_settings.py ]; then
   ln -s local_settings.py.jenkins local_settings.py
fi

#wipe out any *.pyc file to be pedantic
find . -name '*.pyc' -delete

# deploy master code to db
fab test deploy

# recreate the default db
fab test recreate_dev

# fetch data dump from test server
# EDIT: We don't actually have a test server configured with a stable build ... for now we'll make Jenkins run footprint_init to at least make sure the data load parts are working.
#fab test fetch_datadump:force_local_db_destroy:True



#dropdb urbanfootprint
#createdb urbanfootprint --template template_postgis
#python manage.py syncdb --noinput
#
## The following if statement is here because we are not checking-in migrations
## When we do, we should just remove the whole if and let devs deal with migrations
## as well as their resolutions
#MIGRATION_FOLDER=$WORKSPACE/calthorpe/server/calthorpe/footprint/migrations
#
#rm $MIGRATION_FOLDER/0*
#python manage.py schemamigration footprint --initial
#
#python manage.py migrate
#python manage.py collectstatic --noinput
#python manage.py footprint_init

# this triggers the django-jenkins tests, which are set with the JENKINS_TASKS setting in local_settings.py.jenkins
# further documentation is here https://github.com/kmmbvnr/django-jenkins
python manage.py jenkins