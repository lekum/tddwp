from fabric.contrib.files import append
from fabric.api import run, task, sudo, cd

@task
def install_jenkins():
    sudo('export DEBIAN_FRONTEND=noninteractive')
    hostname = run("cat /etc/hostname")
    append("/etc/hosts", "127.0.0.1\t%s" % hostname, use_sudo=True)
    run("wget -q http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key")
    sudo("apt-key add jenkins-ci.org.key")
    append("/etc/apt/sources.list", "deb http://pkg.jenkins-ci.org/debian binary/",
           use_sudo=True)
    sudo("apt-get update -q -y")
    sudo("apt-get install -q -y jenkins")
    sudo("apt-get install -q -y git iceweasel python3 python-virtualenv xvfb")
    # For npm
    sudo("apt-get install -q -y curl build-essential openssl libssl-dev")
    run("git clone https://github.com/joyent/node.git")
    with cd("node"):
        run("./configure")
        run("make")
        sudo("make install")
    run("curl -L -O https://npmjs.org/install.sh")
    sudo("chmod a+x install.sh")
    sudo("./install.sh")
    sudo("npm install -g phantomjs")
