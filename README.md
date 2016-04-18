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
