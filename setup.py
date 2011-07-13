from setuptools import setup
import sys, os

version = '1.0dev'

long_description = (
    open('README.txt').read()
    + '\n' +
    open('CHANGES.txt').read())

setup(name='django_fanstatic',
      version=version,
      description='Fanstatic support for Django.',
      long_description=long_description,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Fanstatic Developers',
      author_email='fanstatic@googlegroups.com',
      url='http://fanstatic.org',
      license='BSD',
      packages=['django_fanstatic'],
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'Django >= 1.2, <1.4',
          'fanstatic',
      ])
