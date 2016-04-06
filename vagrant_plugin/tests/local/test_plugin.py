import os
import unittest

from cloudify.test_utils import workflow_test


class TestPlugin(unittest.TestCase):
    package_path = os.getcwd()
    for i in range(0, 3):
        package_path = os.path.normpath(os.path.join(package_path, '..'))

    plugin_yaml_path = os.path.join(package_path, 'plugin.yaml')
    
    @workflow_test(os.path.join('blueprint', 'vagrant-command-blueprint.yaml'),
                   resources_to_copy=[plugin_yaml_path],
                   inputs={
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
                   })
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
