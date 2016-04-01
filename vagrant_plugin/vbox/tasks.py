import vagrant
import os
from jinja2 import Environment, FileSystemLoader
from cloudify import ctx
from cloudify.decorators import operation
import tempfile

VAGRANTFILE_TEMPLATE = 'Vagrantfile.template'
VBOX_OUTPUT = 'vbox'
VAGRANTFILE_TMP_DIRECTORY = 'cloudify-vagrant-plugin'
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


@operation
def start(vbox_url, **kwargs):
    env = Environment(loader=FileSystemLoader(os.path.join(CURRENT_DIR,
                                                           'resources')))
    template = env.get_template(VAGRANTFILE_TEMPLATE)

    vm = {'vbox_name': kwargs['vbox_name'],
            'vbox_url': vbox_url,
            'vm_name': kwargs['vm_name'],
            'vm_cpus': kwargs['vm_cpus'],
            'vm_memory': kwargs['vm_memory']}
    with open(os.path.join(tempfile.gettempdir(), 'Vagrantfile'), 'w') as f:
        f.write(template.render(vm=vm))

    v = vagrant.Vagrant()
    v.up()
