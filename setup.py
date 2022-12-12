from setuptools import setup, find_packages
import versioneer
import os

def package_files(directory):
    paths = []
    for (path, _, filenames) in os.walk(directory):
        paths.extend(os.path.join('..', path, filename) for filename in filenames)
    return paths

setup(name='clinvoc',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      author='Jason Rudy',
      author_email='jcrudy@gmail.com',
      url='https://github.com/jcrudy/clinvoc',
      include_package_data=True,
#       package_data={
#           'clinvoc.resources': package_files(os.path.join('clinvoc', 'resources')),
#                     },
      packages=find_packages(),
      requires=[],
      install_requires=['toolz', 'pyparsing', 'six', 'multipledispatch', 'terminaltables', 'pandas'],
     )