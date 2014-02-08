from distutils.core import setup

import wadofstuff.django.serializers

README = open('README').read().strip() + "\n\n"
ChangeLog = \
    "What's new\n" + \
    "==========\n" + \
    "\n" + \
    open('ChangeLog').read().strip()
  
LONG_DESCRIPTION = README + ChangeLog

setup(
    name='wadofstuff-django-serializers',
    version=wadofstuff.django.serializers.__version__,
    description='Extended serializers for Django.',
    long_description=LONG_DESCRIPTION,
    author='Matthew Flanagan',
    author_email='mattimustang@gmail.com',
    url='http://code.google.com/p/wadofstuff/',
    download_url='http://wadofstuff.googlecode.com/files/wadofstuff-django-serializers-1.1.0.tar.gz',
    packages=(
        'wadofstuff',
        'wadofstuff.django',
        'wadofstuff.django.serializers',
    ),
    keywords="django json serializer",
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Framework :: Django',
    ),
)

