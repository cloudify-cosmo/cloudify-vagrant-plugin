cloudify-vagrant-plugin
=======================

A Cloudify Plugin that creates and manages virtual machines in virtualbox
## Requirements
## Installation

### Installing VirtualBox

### Installing Vagrant

### Installing Cloudify
To work with this plugin you have to install Cloudify first. Use the documentations found at [Cloudify Guides](http://getcloudify.org/guide/).

### Installing Cloudify Vagrant Plugin

## Usage
The next will be at [Vagrant Plugin](documuntation_to_be_added)

### Locally initializing and deploying Cloudify Vagrant plugins using the CLI
First, create a blueprint using the example provided in the [blueprint creation section](#writing-your-blueprints) along with 
the blueprint inputs.

Second, intialize the Cloudify using `cfy`:
```
cfy init -p <PATH_TO_BLUEPRINT> -i <PATH_TO_INPUTS>
```
At this point the deployment is ready to be deployed. To deploy the deployment:
```
cfy local execute -w install
```
Now the plugin will create, configure and start the virtual machines on your local VirtualBox server. Vagrantfile (the 
vagrant machine configuration file) can be found in your operation system temp file, the directory is named as follows:
```
cloudify-vagrant-plugin-<Random_String>-<Name_Prefix>_<cfy_Instance_ID>
```

## Writing your blueprints
This section will cover writing a blueprint for Cloudify Vagrant Plugin. If you haven't ever written a blueprint for Cloudify, 
you should visit [Cloudify Guides](http://getcloudify.org/guide/) for guidance.

### Imports
The plugin uses Cloudify types and the plugin package itself:
```
imports:
  - http://www.getcloudify.org/spec/cloudify/3.3.1/types.yaml
  - /home/david/development/cloudify-vagrant-plugin/plugin.yaml
```

### Inputs
Vagrant plugin create task accepts the following arguments:
  * **vbox**: VirtualBox box URL or shortened name
  * **vm_name_prefix**: Virtual machine's display name
  * **vm_cpus**: Amount of CPUs to be used by the virtual machine
  * **vm_memory**: Amount of memory to be used by the virtual machine
  * **additional_vagrant_settings**: Accepts a dictionary with vagrant config parameters. The key and
      values will be printed into the Vagrant file as "key= value", at the
      vagrant machine configuration part.
      _Note: Make sure you use 'config.' as the prefix of the configuration key._
  * **additional_virtualbox_settings**: Accepts a dictionary with vagrant config parameters. The key and
          values will be printed into the Vagrant file as "key= value", at
          the virtualbox machine configuration part.
          _Note: Make sure you use 'vbox.' as the prefix of the configuration
          key._
  * **provision_sets**:  A list of dictionaries, each dictionary represents a provision 'set'.
          Each provision 'set' has:
            * **"suffix"** key - a suffix that will appear in Vagrantfile, at the
             provision method.
            * **"type"** key - the provision type (anything that Vagrant accepts).
            * **"provisions"** key - the list of the provision command.
              each command is a dictionary by itself, the key will be the
              Vagrant command and the value will be the command itself.
              For example: `{"inline": "echo Hellow, World"}`

In addition, an IP address can be set by adding an 'ip' property to the virtual machine node. If you provide a CIDR the plugin  
will automatically generate an IP using the CIDR.