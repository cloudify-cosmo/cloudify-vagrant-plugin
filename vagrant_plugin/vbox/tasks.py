import os
import tempfile
import pkg_resources

import vagrant
from jinja2 import Template

from cloudify import ctx
from cloudify.decorators import operation

import utils
import vagrant_plugin

vagrantfile_tempalte = pkg_resources.resource_string(vagrant_plugin.__name__,
                                                     'resources/' +
                                                     'vbox/' +
                                                     'Vagrantfile.template')
VAGRANTFILE_TMP_DIRECTORY_PREFIX = 'cloudify-vagrant-plugin-'
VAGRANT_SSH_PRIVATE_KEY_FILE_PATH = os.path.join('.vagrant', 'machines',
                                                 'default', 'virtualbox',
                                                 'private_key')


@operation
def create(**kwargs):
    instance_id = ctx.instance.id
    template = Template(vagrantfile_tempalte)

    vm_conf = {'vbox': kwargs['vbox'],
          'vm_name_prefix':
              '{0}_{1}'.format(kwargs['vm_name_prefix'], instance_id),
          'vm_cpus': kwargs['vm_cpus'],
          'vm_memory': kwargs['vm_memory'],
          'ip': utils.set_ip(ctx.node.properties['ip'],
                             node_id_seed=ctx.node.id),
          'additional_vagrant_settings': utils.parse_additional_settings(
                  kwargs['additional_vagrant_settings'], indents=1),
          'additional_virtualbox_settings': utils.parse_additional_settings(
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

    v = vagrant.Vagrant(root=output_path_dir, quiet_stdout=False)

    ctx.logger.info('Initializing and running "vagrant up" for {0}...'.format(
            ctx.instance.id))
    v.up(no_provision=True)


@operation
def configure(**kwargs):
    ctx.logger.info('Running "vagrant provision" for {0}...'.format(
            ctx.instance.id))
    v = vagrant.Vagrant(root=ctx.instance.runtime_properties['output_path'])
    v.provision()
