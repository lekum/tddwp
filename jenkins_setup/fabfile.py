from fabric.contrib.files import append
from fabric.api import run, task, sudo

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
