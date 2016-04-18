cloudify-vagrant-plugin
=======================

A Cloudify Plugin that creates and manages virtual machines in virtualbox

## Usage
The next will be at [Vagrant Plugin](documuntation_to_be_added)

### Installing Cloudify
To work with this plugin you have to install Cloudify first. Use the documentations found at [Cloudify Guides](http://getcloudify.org/guide/).

### Locally initializing and deploying Cloudify Vagrant plugins using the CLI
First, create a blueprint using the example provided in the [blueprint creation section](#"Blueprint Example") along with 
the blueprint inputs.

Second, intialize the Cloudify using the ```cfy``` command:
```
cfy init -p <PATH_TO_BLUEPRINT> -i <PATH_TO_INPUTS>
```
At this point the 

## Requirements
Vagrant 1.8.1