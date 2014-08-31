# LATEST STUFF TODO integrate with older stuff belo
irst download gdal:

pip install --no-install GDAL
then specify where the headers are:

python setup.py build_ext --include-dirs=/usr/include/gdal/
then install it:

pip install --no-download GDAL
Here's another way to install gdal python:

$ sudo apt-add-repository ppa:ubuntugis/ubuntugis-unstable
$ sudo apt-get update
$ sudo apt-get install python-gdal
after that open IDLE:

from osgeo import gdal

# Python mapnik library binding
sudo add-apt-repository ppa:mapnik/nightly-2.0
sudo apt-get update
sudo apt-get install libmapnik mapnik-utils python-mapnik

# Soft link to the mapnik dir since it's not in the search path of the virtualenv python
cd /srv/calthorpe_env/lib/python2.7/site-packages
ln -s /usr/lib/pymodules/python2.7/mapnik
ln -s /usr/lib/python2.7/dist-packages/osgeo/

sudo apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev
sudo pip install -U werkzeug
sudo pip install -U simplejson
sudo pip install -U modestmaps 
sudo pip install -U pil
sudo pip install numpy

# These are needed by pil. Use i386 instead of x86_64 for 32 bit machines
cde /usr/lib
sudo ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib/
sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/
sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/

# TileStache install
cd ~/tmp
git clone https://github.com/migurski/TileStache.git
cd TileStache/
python setup.py install

# Install apache2
sudo apt-get apache2
sudo apt-get install libapache2-mod-wsgi
sudo a2enmod wsgi

# Point apache2 to the tile_stache conf file
cd /etc/apache2
sudo rm httpd.conf
sudo ln -s /srv/calthorpe/urban_footprint/calthorpe/server/conf/tilestache.apache sites_available/
sudo ln -s /srv/calthorpe/urban_footprint/calthorpe/server/conf/tilestache.apache sites_enabled/

mkdir /var/www/tiles


sudo apache2ctl restart

