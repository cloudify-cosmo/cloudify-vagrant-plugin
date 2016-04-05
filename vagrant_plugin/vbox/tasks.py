import vagrant
import os
from jinja2 import Environment, FileSystemLoader
from cloudify import ctx
from cloudify.decorators import operation
import tempfile

VAGRANTFILE_TEMPLATE = 'Vagrantfile.template'
VAGRANTFILE_TMP_DIRECTORY = 'cloudify-vagrant-plugin'
VBOX_RESOURCE_PATH = os.path.join('resources', 'vbox')
CURRENT_DIR = os.getcwd()


def return_vbox_conf(**kwargs):
    try:
        return 'config.vm.box = {0}'.format(kwargs['vbox_name'])
    except KeyError:
        try:
            return 'config.vm.box_url = {0}'.format(kwargs['vbox_url'])
        except KeyError:
            print IOError('No vagrant box url nor name provided')


@operation
def start(**kwargs):
    instance_id = ctx.instance.id
    env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(CURRENT_DIR),
                                             VBOX_RESOURCE_PATH)))
    template = env.get_template(VAGRANTFILE_TEMPLATE)

    vm = {'vbox_conf': return_vbox_conf(kwargs),
          'vm_name_prefix':
              '{0}_{1}'.format(kwargs['vm_name_prefix'], instance_id),
          'vm_cpus': kwargs['vm_cpus'],
          'vm_memory': kwargs['vm_memory'],
          'vm_ip_address': kwargs['vm_ip_address']}

    output_path = tempfile.mkdtemp(prefix=VAGRANTFILE_TMP_DIRECTORY, suffix='-' + instance_id)
    ctx.logger.info('"{0}" path has been created'.format(output_path))

    with open(os.path.join(output_path, 'Vagrantfile'), 'w') as f:
        f.write(template.render(vm=vm))

    ctx.logger.info('Initializing Vagrant for {0}'.format(instance_id))
    v = vagrant.Vagrant(root=output_path)
    ctx.logger.info('Running "vagrant up" for {0}'.format(instance_id))
    v.up()
