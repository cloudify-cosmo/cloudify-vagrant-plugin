import os
import random
import tempfile
import pkg_resources

import vagrant
from jinja2 import Template
from netaddr import IPNetwork

from cloudify import ctx
from cloudify.decorators import operation

import vagrant_plugin

VAGRANTFILE_TMP_DIRECTORY_PREFIX = 'cloudify-vagrant-plugin-'
VAGRANT_SSH_PRIVATE_KEY_FILE_PATH = os.path.join(
        '.vagrant', 'machines', 'default', 'virtualbox', 'private_key')


def _parse_additional_settings(additional_settings, indents):
    string_buffer = ''
    for key, value in additional_settings.items():
        string_buffer += '\n{0}{1}= "{2}"'.format('\t' * indents, key, value)
    return string_buffer


def _set_ip(cidr, node_id_seed=None):
    if cidr:
        # IPNetwork with an IP address returns the IP address
        return str(random.choice(IPNetwork(cidr)))
    else:
        return _gen_rand_ip(seed=node_id_seed)


def _gen_rand_ip(seed=None):
    not_valid = [10, 127, 169, 172, 192]

    random.seed(seed)
    first = random.randrange(1, 256)
    while first in not_valid:
        first = random.randrange(1, 256)

    # Use seed only for the first three
    second = random.randrange(1, 256)
    third = random.randrange(1, 256)
    random.seed(None)
    return ".".join(
            [str(first), str(second), str(third),
             str(random.randrange(1, 256))])


@operation
def create(**kwargs):
    instance_id = ctx.instance.id
    template = Template(
            pkg_resources.resource_string(
                    vagrant_plugin.__name__,
                    os.path.join('resources', 'vbox', 'Vagrantfile.template'))
    )

    vm_conf = {
        'vbox': kwargs['vbox'],
        'vm_name_prefix': '{0}_{1}'.format(
                kwargs['vm_name_prefix'], instance_id),
        'vm_cpus': kwargs['vm_cpus'],
        'vm_memory': kwargs['vm_memory'],
        'ip': _set_ip(
                ctx.node.properties['ip'], node_id_seed=ctx.node.id),
        'additional_vagrant_settings': _parse_additional_settings(
                kwargs['additional_vagrant_settings'], indents=1),
        'additional_virtualbox_settings': _parse_additional_settings(
                kwargs['additional_virtualbox_settings'], indents=2),
        'provision_sets': kwargs['provision_sets']
    }

    ctx.logger.debug('Creating output tmp dir')
    output_path_dir = tempfile.mkdtemp(prefix=VAGRANTFILE_TMP_DIRECTORY_PREFIX,
                                       suffix='-' + instance_id)

    ctx.logger.debug('Saving output tmp dir to runtime properties')
    ctx.instance.runtime_properties['output_path_dir'] = output_path_dir

    ctx.logger.debug('Saving IP to runtime properties')
    ctx.instance.runtime_properties['ip'] = vm_conf['ip']

    ctx.logger.debug('Saving ssh key path to runtime properties')
    ctx.instance.runtime_properties['ssh_key'] = \
        os.path.join(output_path_dir, VAGRANT_SSH_PRIVATE_KEY_FILE_PATH)

    with open(os.path.join(output_path_dir, 'Vagrantfile'), 'w') as f:
        f.write(template.render(vm_conf=vm_conf))

    _run_vagrant_command('up', quiet_stdout=False, no_provision=True)


def _run_vagrant_command(command, **kwargs):
    vagrant_file_path = ctx.instance.runtime_properties['output_path_dir']

    ctx.logger.info('Running "Vagrant {0}"'.format(command))
    v = vagrant.Vagrant(root=vagrant_file_path, **kwargs)

    getattr(v, command)(**kwargs)


@operation
def configure(**kwargs):
    ctx.logger.info('Running "vagrant provision" for {0}...'.format(
            ctx.instance.id))
    v = vagrant.Vagrant(root=ctx.instance.runtime_properties[
        'output_path_dir'])
    v.provision()


@operation
def start(**kwargs):
    ctx.logger.info('Running "vagrant up" for {0}...'.format(
            ctx.instance.id))
    v = vagrant.Vagrant(root=ctx.instance.runtime_properties[
        'output_path_dir'])
    v.up(no_provision=True)


@operation
def stop(**kwargs):
    ctx.logger.info('Running "vagrant halt" for {0}...'.format(
            ctx.instance.id))
    v = vagrant.Vagrant(root=ctx.instance.runtime_properties[
        'output_path_dir'])
    v.halt()


@operation
def delete(**kwargs):
    vagrant_file_path = ctx.instance.runtime_properties['output_path_dir']

    ctx.logger.info('Running "vagrant destroy" for {0}...'.format(
            ctx.instance.id))
    v = vagrant.Vagrant(root=vagrant_file_path)
    v.destroy()
