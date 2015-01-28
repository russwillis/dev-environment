# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # vagrantup.com

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "landregistry/ubuntu"

  # Once the server has booted, run the following shell script
  config.vm.provision :shell, :path => 'provision.sh'

  # Shares the app folder
  config.vm.synced_folder "apps", "/home/vagrant/apps/"

  # Flask Port
  config.vm.network :forwarded_port, host: 5000, guest: 5000

  # PostgreSQL Server port forwarding
  config.vm.network :forwarded_port, host: 5432, guest: 5432
  config.vm.network :forwarded_port, host: 15432, guest: 15432

end
