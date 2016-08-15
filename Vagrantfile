VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
	config.vm.box = "ubuntu/trusty64"
	config.vm.network :forwarded_port, guest: 80, host: 8080
	config.vm.network "private_network", ip: "10.0.0.5"
	config.vm.synced_folder ".", "/ads"
	config.vm.provision "ansible" do |ansible|
		ansible.playbook = "provision/provision.yml"
	end
end
