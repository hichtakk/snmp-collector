from setuptools import setup
from codecs import open
import os
import re

version = ''
with open('toami/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)
if not version:
    raise RuntimeError('Cannot find version information')

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

requires = []
def _load_requires(path):
    return requires + [pkg.rstrip('\r\n') for pkg in open(path).readlines()]
    
setup(
    name='Toami',
    version=version,
    description='SNMP asyncronous collector',
    long_description=long_description,
    url='https://github.com/hichtakk/toami',
    author='hichtakk',
    author_email='hichtakk@gmail.com',
    license='apache',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='network snmp',
    install_requires=_load_requires('requirements.txt'),
    packages=['toami'],
    package_data={
        'sample': ['config.json.sample']
    },
    scripts=['bin/toami']
)
