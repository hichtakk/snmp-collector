from distutils.core import setup

requires = []
def _load_requires(path):
    print([pkg.rstrip('\r\n') for pkg in open(path).readlines()])
    return requires + [pkg.rstrip('\r\n') for pkg in open(path).readlines()]
    
setup(
    name='SNMPCollector',
    version='0.1',
    description='SNMP asyncronous collector',
    long_description='SNMP asyncronous collector',
    url='https://github.com/hichtakk/snmp-collector',
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
    package_data={
        'sample': ['config.json.sample']
    }
)
