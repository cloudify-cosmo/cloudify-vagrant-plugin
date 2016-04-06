import os
import unittest

from cloudify.test_utils import workflow_test


def get_n_dir_back(path, multiplier=1):
    for i in range(0, multiplier):
        path = os.path.normpath(os.path.join(path, '..'))
    return path


PACKAGE_PATH = get_n_dir_back(os.getcwd(), multiplier=3)
PLUGIN_YAML_PATH = os.path.join(PACKAGE_PATH, 'plugin.yaml')
BLUEPRINT_PATH = \
    os.path.join(os.path.dirname(os.getcwd()),
                 os.path.join('blueprint',
                              'vagrant-command-blueprint.yaml'))


@staticmethod
def get_inputs(test_method):
    inputs = {'test_my_task': {
        'vbox': 'file:///home/david/Downloads/precise64.box',
        'vm_name_prefix': 'test',
        'vm_cpus': '2',
        'vm_memory': '1024',
        'vm_ip_address': '192.0.2.0/23',
        'additional_vagrant_settings': {},
        'additional_virtualbox_settings': {},
        'provision_sets': [
            {'suffix': 'shell', 'type': 'shell', 'provisions':
                [
                    {'inline': 'echo hello world!'},
                    {'inline': 'echo hello again!'}]}
        ]
    }

    @workflow_test(BLUEPRINT_PATH,
                   resources_to_copy=[PLUGIN_YAML_PATH],
                   inputs=inputs)
    def test_my_task(self, cfy_local):
        # execute install workflow
        """
        :param cfy_local:
        """
        cfy_local.execute('install', task_retries=0)

        # extract single node instance
        instance = cfy_local.storage.get_node_instances()[0]

        # assert runtime properties is properly set in node instance
        self.assertEqual(instance.runtime_properties['some_property'],
                         'new_test_input')

        # assert deployment outputs are ok
        self.assertDictEqual(cfy_local.outputs(), inputs)
