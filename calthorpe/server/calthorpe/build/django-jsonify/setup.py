from distutils.core import setup

fhandler = open('README.rst', 'r')
long_desc = fhandler.read()
fhandler.close()

setup(name='django-jsonify',
      packages=['jsonify', 'jsonify.templatetags'],
      version='0.2.1',
      description="Django additions for JSON",
      long_description=long_desc,
      author='Marius Grigaitis',
      author_email='m@mar.lt',
      license='BSD',
      keywords=['json', 'django', 'jsonify'],
      requires=['django'],
      url='https://bitbucket.org/marltu/django-jsonify/',
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Plugins',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'Framework :: Django',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Topic :: Utilities'])
