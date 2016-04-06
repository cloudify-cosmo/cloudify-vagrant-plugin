import utils
import unittest

from cloudify.test_utils import workflow_test


class TestPlugin(unittest.TestCase):
    @workflow_test(utils.BLUEPRINT_PATH,
                   resources_to_copy=[utils.PLUGIN_YAML_PATH],
                   inputs=utils.get_inputs('test_my_task'))
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
        self.assertDictEqual(cfy_local.outputs(), get_inputs('test_my_task'))
