from setuptools import setup

setup(
    name='cloudify-vagrant-plugin',
    version='1.0',
    author='Gigaspaces',
    author_email='cosmo-admin@gigaspaces.com',
    packages=['vagrant_plugin', 'vagrant_plugin/vbox'],
    license='LICENSE',
    description='Plugin for running vagrant tasks',
    install_requires=[
        'cloudify-plugins-common>=3.3.1',
        'jinja2',
        'python-vagrant'
    ]
)