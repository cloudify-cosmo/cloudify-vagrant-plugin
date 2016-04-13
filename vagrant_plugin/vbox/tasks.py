import vagrant
import os
from jinja2 import Environment, FileSystemLoader
from cloudify import ctx
from cloudify.decorators import operation
import tempfile
import utils
import vagrant_plugin

VAGRANTFILE_TEMPLATE = 'Vagrantfile.template'
VAGRANTFILE_TEMPLATE_PATH = os.path.join(
        os.path.dirname(vagrant_plugin.__file__), 'resources', 'vbox')
VAGRANTFILE_TMP_DIRECTORY = 'cloudify-vagrant-plugin-'
VAGRANT_SSH_PRIVATE_KEY_PATH = os.path.join('.vagrant', 'machines', 'default',
                                            'virtualbox', 'private_key')


@operation
def start(**kwargs):
    instance_id = ctx.instance.id
    env = Environment(
            loader=FileSystemLoader(VAGRANTFILE_TEMPLATE_PATH))
    template = env.get_template(VAGRANTFILE_TEMPLATE)

    # TODO convert provision_sets['provisions'] to an ordered collection
    vm = {'vbox': kwargs['vbox'],
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

    output_path = tempfile.mkdtemp(prefix=VAGRANTFILE_TMP_DIRECTORY,
                                   suffix='-' + instance_id)
    ctx.logger.info('"{0}" path has been created'.format(output_path))
    ctx.instance.runtime_properties['output_path'] = output_path
    ctx.logger.info('"{0}" path has been saved to runtime properties'.format(
            output_path))
    ctx.instance.runtime_properties['ip'] = vm['ip']
    ctx.logger.info('"{0}" ip has been saved to runtime properties'.format(
            vm['ip']))
    ctx.node.properties['cloudify_agent']['key'] = \
        os.path.join(output_path, VAGRANT_SSH_PRIVATE_KEY_PATH)
    with open(os.path.join(output_path, 'Vagrantfile'), 'w') as f:
        f.write(template.render(vm=vm))

    ctx.logger.info('Initializing Vagrant for {0}'.format(instance_id))
    v = vagrant.Vagrant(root=output_path)
    ctx.logger.info('Running "vagrant up" for {0}'.format(instance_id))
    # v.up(no_provision=True) TODO use separate workflow for provisioning
    v.up()


@operation
def config(**kwargs):
    ctx.logget.info('Running "vagrant provision" for {0}'.format(
            ctx.instance.id))
    v = vagrant.Vagrant(root=ctx.instance.runtime_properties['output_path'])
    v.provision()
