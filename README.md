cloudify-vagrant-plugin
=======================

A Cloudify Plugin that creates and manages virtual machines in virtualbox

## Installation

### Installing VirtualBox

### Installing Vagrant

### Installing Cloudify
To work with this plugin you have to install Cloudify first. Use the documentations found at [Cloudify Guides](http://getcloudify.org/guide/).

## Usage
The next will be at [Vagrant Plugin](documuntation_to_be_added)

### Locally initializing and deploying Cloudify Vagrant plugins using the CLI
First, create a blueprint using the example provided in the [blueprint creation section](#"Blueprint Example") along with 
the blueprint inputs.

Second, intialize the Cloudify using `cfy`:
```
cfy init -p <PATH_TO_BLUEPRINT> -i <PATH_TO_INPUTS>
```
At this point the deployment is ready to be deployed. To deploy the deployment:
```
cfy local execute -w install
```
Now 

## Requirements
Vagrant 1.8.1