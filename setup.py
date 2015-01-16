import os
from setuptools import setup

def fread(filename):
  return open(os.path.join(os.path.dirname(__file__), filename)).read()

def get_version():
  return fread('VERSION')

setup(
    name='pycapa',
    version=get_version(),
    author='Tom Piscitell',
    author_email='tpiscite@cisco.com',
    description='Tool for capturing packets with OpenSOC',
    long_description=fread('README.md'),
    entry_points = {
      "console_scripts" : [ 'pycapa = pycapa.pycapa_cli:main' ],
      },
    packages = [ 'pycapa' ]
    )

