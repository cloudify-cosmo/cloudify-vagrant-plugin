import vagrant
import os
from jinja2 import Environment, FileSystemLoader
from cloudify import ctx
from cloudify.decorators import operation
import tempfile

VAGRANTFILE_TEMPLATE = 'Vagrantfile.template'
VAGRANTFILE_TMP_DIRECTORY = 'cloudify-vagrant-plugin'
VBOX_RESOURCE_PATH = os.path.join('resources', 'vbox')
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


@operation
def start(vbox_url, **kwargs):
    instance_id = ctx.instance.id
    env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(CURRENT_DIR),
                                                 VBOX_RESOURCE_PATH)))
    template = env.get_template(VAGRANTFILE_TEMPLATE)

    vm = {'vbox_name': kwargs['vbox_name'],
          'vbox_url': vbox_url,
          'vm_name_prefix':
              '{}_{}'.format(kwargs['vm_name_prefix'], instance_id),
          'vm_cpus': kwargs['vm_cpus'],
          'vm_memory': kwargs['vm_memory'],
          'vm_ip_address': kwargs['vm_ip_address']}
    output_path = os.path.join(tempfile.gettempdir(),
                               VAGRANTFILE_TMP_DIRECTORY,
                               'vagrantfile-{}'.format(
                                       instance_id))
    if not os.path.exists(output_path):
        while True:
            try:
                os.makedirs(output_path)
                ctx.logger.info('\'{}\' path has been created'
                                .format(output_path))
                break
            except OSError as exc:
                ctx.logger.info('OSError ignored')
                pass
    with open(os.path.join(output_path, 'Vagrantfile'), 'w') as f:
        f.write(template.render(vm=vm))

    ctx.logger.info('initializing Vagrant for {}'.format(instance_id))
    v = vagrant.Vagrant(root=output_path)
    ctx.logger.info('running \'vagrant up\' for {}'.format(instance_id))
    v.up()
