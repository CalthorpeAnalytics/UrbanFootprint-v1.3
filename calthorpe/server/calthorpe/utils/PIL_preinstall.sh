# -------------------
#
# PIL installation
#
# -------------------

# thanks to Sanders New Media for the method
# http://www.sandersnewmedia.com/why/2012/04/16/installing-pil-virtualenv-ubuntu-1204-precise-pangolin/

# install the build dependencies
apt-get build-dep python-imaging

# create symlinks from the deps to a place where PIL will find them
ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/
ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/
ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/

apt-get install PIL

# -------------------
#
# Mapnik installation
#
# -------------------

# Install icu

wget http://download.icu-project.org/files/icu4c/4.6/icu4c-4_6-src.tgz
tar xzvf icu4c-4_6-src.tgz
cd icu/source
./runConfigureICU Linux
make
sudo make install
sudo ldconfig

# Install Boost

sudo add-apt-repository ppa:mapnik/boost
sudo apt-get update
sudo apt-get install libboost-dev libboost-filesystem-dev libboost-program-options-dev libboost-python-dev libboost-regex-dev libboost-system-dev libboost-thread-dev


