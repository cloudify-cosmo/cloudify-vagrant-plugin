[1mdiff --git a/vagrant_plugin/vbox/tasks.py b/vagrant_plugin/vbox/tasks.py[m
[1mindex 6c51564..dce0ab9 100644[m
[1m--- a/vagrant_plugin/vbox/tasks.py[m
[1m+++ b/vagrant_plugin/vbox/tasks.py[m
[36m@@ -12,14 +12,13 @@[m [mfrom cloudify.decorators import operation[m
 [m
 import vagrant_plugin[m
 [m
[31m-vagrantfile_tempalte = pkg_resources.resource_string(vagrant_plugin.__name__,[m
[31m-                                                     'resources/' +[m
[31m-                                                     'vbox/' +[m
[31m-                                                     'Vagrantfile.template')[m
[32m+[m[32mvagrantfile_template = \[m
[32m+[m[32m    pkg_resources.resource_string([m
[32m+[m[32m            vagrant_plugin.__name__,[m
[32m+[m[32m            os.path.join('resources', 'vbox', 'Vagrantfile.template'))[m
 VAGRANTFILE_TMP_DIRECTORY_PREFIX = 'cloudify-vagrant-plugin-'[m
[31m-VAGRANT_SSH_PRIVATE_KEY_FILE_PATH = os.path.join('.vagrant', 'machines',[m
[31m-                                                 'default', 'virtualbox',[m
[31m-                                                 'private_key')[m
[32m+[m[32mVAGRANT_SSH_PRIVATE_KEY_FILE_PATH = os.path.join([m
[32m+[m[32m        '.vagrant', 'machines', 'default', 'virtualbox', 'private_key')[m
 [m
 [m
 def _parse_additional_settings(additional_settings, indents):[m
[36m@@ -57,21 +56,22 @@[m [mdef _gen_rand_ip(seed=None):[m
 @operation[m
 def create(**kwargs):[m
     instance_id = ctx.instance.id[m
[31m-    template = Template(vagrantfile_tempalte)[m
[31m-[m
[31m-    vm_conf = {'vbox': kwargs['vbox'],[m
[31m-               'vm_name_prefix': '{0}_{1}'.format(kwargs['vm_name_prefix'],[m
[31m-                                                  instance_id),[m
[31m-               'vm_cpus': kwargs['vm_cpus'],[m
[31m-               'vm_memory': kwargs['vm_memory'],[m
[31m-               'ip': _set_ip(ctx.node.properties['ip'],[m
[31m-                            node_id_seed=ctx.node.id),[m
[31m-               'additional_vagrant_settings': _parse_additional_settings([m
[31m-                       kwargs['additional_vagrant_settings'], indents=1),[m
[31m-               'additional_virtualbox_settings': _parse_additional_settings([m
[31m-                       kwargs['additional_virtualbox_settings'], indents=2),[m
[31m-               'provision_sets': kwargs['provision_sets'][m
[31m-               }[m
[32m+[m[32m    template = Template(vagrantfile_template)[m
[32m+[m
[32m+[m[32m    vm_conf = {[m
[32m+[m[32m        'vbox': kwargs['vbox'],[m
[32m+[m[32m        'vm_name_prefix': '{0}_{1}'.format([m
[32m+[m[32m                kwargs['vm_name_prefix'], instance_id),[m
[32m+[m[32m        'vm_cpus': kwargs['vm_cpus'],[m
[32m+[m[32m        'vm_memory': kwargs['vm_memory'],[m
[32m+[m[32m        'ip': _set_ip([m
[32m+[m[32m                ctx.node.properties['ip'], node_id_seed=ctx.node.id),[m
[32m+[m[32m        'additional_vagrant_settings': _parse_additional_settings([m
[32m+[m[32m                kwargs['additional_vagrant_settings'], indents=1),[m
[32m+[m[32m        'additional_virtualbox_settings': _parse_additional_settings([m
[32m+[m[32m                kwargs['additional_virtualbox_settings'], indents=2),[m
[32m+[m[32m        'provision_sets': kwargs['provision_sets'][m
[32m+[m[32m    }[m
 [m
     ctx.logger.debug('Creating output tmp dir')[m
     output_path_dir = tempfile.mkdtemp(prefix=VAGRANTFILE_TMP_DIRECTORY_PREFIX,[m
[36m@@ -97,6 +97,13 @@[m [mdef create(**kwargs):[m
     v.up(no_provision=True)[m
 [m
 [m
[32m+[m[32mdef _run_vagrant_command(command, **kwargs):[m
[32m+[m[32m    ctx.logger.info('Running "Vagrant {0}"'.format(command))[m
[32m+[m[32m    v = vagrant.Vagrant(root=None)[m
[32m+[m
[32m+[m[32m    getattr(v, command)(**kwargs)[m
[32m+[m
[32m+[m
 @operation[m
 def configure(**kwargs):[m
     ctx.logger.info('Running "vagrant provision" for {0}...'.format([m
[36m@@ -126,8 +133,9 @@[m [mdef stop(**kwargs):[m
 [m
 @operation[m
 def delete(**kwargs):[m
[32m+[m[32m    vagrant_file_path = ctx.instance.runtime_properties['output_path_dir'][m
[32m+[m
     ctx.logger.info('Running "vagrant destroy" for {0}...'.format([m
             ctx.instance.id))[m
[31m-    v = vagrant.Vagrant(root=ctx.instance.runtime_properties[[m
[31m-        'output_path_dir'])[m
[32m+[m[32m    v = vagrant.Vagrant(root=vagrant_file_path)[m
     v.destroy()[m
