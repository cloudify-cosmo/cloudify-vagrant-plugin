from setuptools import setup, find_packages

setup(
    name='cloudify-vagrant-plugin',
    version='0.1',
    author='Gigaspaces',
    author_email='cosmo-admin@gigaspaces.com',
    packages=find_packages(exclude=["tests"]),
    package_dir={'vagrant_plugin': 'vagrant_plugin'},
    package_data={'vagrant_plugin': ['resource/vbox/Vagrantfile.template']},
    license='LICENSE',
    description='Plugin for running vagrant tasks',
    install_requires=[
        'cloudify-plugins-common>=3.3.1',
        'jinja2==2.7.2',
        'python-vagrant==0.5.11',
        'netaddr==0.7.18'
    ]
)