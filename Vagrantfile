# -*- coding: utf-8 -*-
# -*- mode: ruby -*-
# vi: set ft=ruby :
#
# Shared Folders
# --------------
# => http://docs.vagrantup.com/v2/synced-folders/index.html
#
# Customize Machine Settings
# --------------------------
# => http://docs.vagrantup.com/v2/providers/configuration.html
# => http://docs.vagrantup.com/v2/virtualbox/configuration.html
# => http://docs.vagrantup.com/v2/vmware-fusion/configuration.html
#
# Provisioning
# ------------
# => http://docs.vagrantup.com/v2/provisioning/shell.html
# => http://docs.vagrantup.com/v2/provisioning/puppet_apply.html
# => http://docs.vagrantup.com/v2/provisioning/puppet_agent.html
#

Vagrant.configure("2") do |config|

  # Name of the vagrant box
  config.vm.box = 'precise-server-cloudimg-vagrant-amd64-disk1'

  # URL where to download the vagrant box from
  # The basebox is on https://spotify.box.com/vagrant-box-debian-squeeze-64
  # However it requires you to download it manually.
  # todo: figure out the direct box download URL to place here
  config.vm.box_url = 'http://cloud-images.ubuntu.com/precise/current/precise-server-cloudimg-vagrant-amd64-disk1.box'

  # Define the machine named default
  # For multi machine setup, duplicate the block below defining different names
  # e.g. web, database, etc. See: http://docs.vagrantup.com/v2/multi-machine/index.html
  config.vm.define :default do |machine|
    # Hostname of the machine
    machine.vm.hostname = 'feedduty.dev.bkuberek.com'

    # This is the IP address of your VM.
    # You will be able to access the machine via this IP
    machine.vm.network :private_network, ip: "13.10.20.18"

    ###########################################################################
    # Synced Folders                                                          #
    ###########################################################################

    # vagrnat will mount this regardless. So lets us mount it as NFS and use it.
    machine.vm.synced_folder ".", "/vagrant"

    ###########################################################################
    # Guest Machine Customization                                             #
    ###########################################################################

    machine.vm.provider :virtualbox do |p|
      p.gui = false
      p.customize ["modifyvm", :id, "--memory", 1024]
    end

    machine.vm.provider :vmware do |p|
      p.gui = false
      p.disable_setuid = true
      p.vmx["memsize"] = "1024"
    end

    ###########################################################################
    # Machine Provisioning                                                    #
    ###########################################################################

    # add a shell or other machine specific provisioning here
  end

  #############################################################################
  # Global Provisioning                                                       #
  #############################################################################

  #config.vm.provision :spotify
end
