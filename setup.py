#!/usr/bin/env python

from distutils.core import setup

setup(name='Distutils',
      version='1.0',
      description='Python Distribution Utilities',
      author='Andy',
      author_email='aking1012.com@gmail.com',
      url='http://github.com/aking1012/python3-stockdbsync',
      packages=['stockDbSync', 'stockDbSync.acquisition', 'stockDbSync.djangoORM', 'stockDbSync.stockmodels'],
      package_dir={'stockDbSync': 'stockDbSync'},
      package_data={'stockDbSync': ['scripts/configdb.bash', 'scripts/dbsettings.bash', 'scripts/dbsettings.py', 'example/example.py']}
      )
