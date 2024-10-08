DOCKER_BUILD_DIR = ENV['DOCKER_BUILD_DIR']
DOCKER_FILE_PATH = ENV['DOCKER_FILE_PATH']
DOCKER_IMAGE_URI = ENV['DOCKER_IMAGE_URI']

OUTPUT_DIR_HOST = ENV['OUTPUT_DIR_HOST']
OUTPUT_DIR_GUEST = ENV['OUTPUT_DIR_GUEST']
OUTPUT_FILENAME = ENV['OUTPUT_FILENAME']


Vagrant.configure("2") do |config|
  config.vm.define "hashicorp" do |h|
    h.vm.box = "hashicorp/bionic64"
    h.vm.disk :disk, size: "128GB", primary: true
    h.vm.synced_folder "#{OUTPUT_DIR_HOST}", "#{OUTPUT_DIR_GUEST}"
  end

  config.vm.provider "virtualbox" do |v|
    v.memory = 8096
    v.cpus = 8
  end

  resize = <<-SCRIPT
  sudo parted /dev/sda resizepart 1 100%
  sudo pvresize /dev/sda1
  sudo lvresize --resizefs -l +100%FREE vagrant-vg/root
  SCRIPT
  config.vm.provision :shell, :inline => resize

  config.vm.provision "docker" do |d|
    d.build_image "-t #{DOCKER_IMAGE_URI} -f #{DOCKER_FILE_PATH} #{DOCKER_BUILD_DIR}"
  end

  config.vm.provision "shell",
    inline: "docker save --output #{OUTPUT_DIR_GUEST}/#{OUTPUT_FILENAME} #{DOCKER_IMAGE_URI}"

end
