from setuptools import setup


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
              'testproject = testproject.resource:library',
              ],
          },
      )
