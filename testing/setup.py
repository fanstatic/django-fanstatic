from setuptools import setup
import setuptools

setup=setuptools.setup

setup(name='testproject',
      version='1.0dev',
      description='testproject',
      packages=['testproject'],
      install_requires=[
          'fanstatic',
          'Django',
      ],
      entry_points={
          'fanstatic.libraries': [
              'testapp = testproject.testapp.resource:library',
              ],
          },
      )
