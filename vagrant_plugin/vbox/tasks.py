import vagrant
import os
from jinja2 import Environment, FileSystemLoader
from cloudify import ctx
from cloudify.decorators import operation
import tempfile

VAGRANTFILE_TEMPLATE = 'Vagrantfile.template'
VAGRANTFILE_TMP_DIRECTORY = 'cloudify-vagrant-plugin'
VBOX_RESOURCE_PATH = 'resources/vbox'
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


@operation
def start(vbox_url, **kwargs):
    env = Environment(
            loader=FileSystemLoader(os.path.join(CURRENT_DIR,
                                                 os.path.pardir,
                                                 VBOX_RESOURCE_PATH)))
    template = env.get_template(VAGRANTFILE_TEMPLATE)

    vm = {'vbox_name': kwargs['vbox_name'],
          'vbox_url': vbox_url,
          'vm_name': kwargs['vm_name'],
          'vm_cpus': kwargs['vm_cpus'],
          'vm_memory': kwargs['vm_memory']}
    output_path = os.path.join(tempfile.gettempdir(),
                               VAGRANTFILE_TMP_DIRECTORY,
                               'Vagrantfile-{}'.format(ctx.node.properties[
                                                           'id']))
    with open(output_path, 'w') as f:
        f.write(template.render(vm=vm))

    v = vagrant.Vagrant()
    v.up()
