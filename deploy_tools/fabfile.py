from fabric.contrib.files import append, exists, sed, upload_template
from fabric.api import env, local, run, task, sudo
import random

REPO_URL = 'https://github.com/lekum/tddwp'

@task
def provision_and_deploy():
    install_prerequisites()
    deploy()
    context = {'app_user': env.user,
     'host': env.host,
     'app_url': env.app_url}
    configure_nginx(context)
    configure_gunicorn_supervisor(context)
    restart_supervisor_nginx()


@task
def deploy():
    site_folder = '/home/%s/sites/%s' % (env.user, env.app_url)
    source_folder = site_folder + '/source'
    create_directory_structure_if_necessary(site_folder)
    get_latest_source(source_folder)
    update_settings(source_folder, env.app_url)
    update_virtualenv(source_folder)
    update_static_files(source_folder)
    update_database(source_folder)

def install_prerequisites():
    sudo('export DEBIAN_FRONTEND=noninteractive')
    sudo('apt-get update && apt-get install -q -y nginx git python3 python3-pip supervisor')
    sudo('pip3 install virtualenv')


def create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))


def get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % (source_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))


def update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(settings_path, 'DOMAIN = "localhost"', 'DOMAIN = "%s"' % (site_name,))
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghi pqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join((random.SystemRandom().choice(chars) for _ in range(50)))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (virtualenv_folder, source_folder))


def update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python manage.py collectstatic --noinput' % (source_folder,))


def update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python manage.py migrate --noinput' % (source_folder,))


def configure_nginx(context):
    upload_template('./nginx.conf.j2', '/etc/nginx/sites-available/%s' % env.app_url, context=context, use_jinja=True, use_sudo=True)
    destination_link = "/etc/nginx/sites-enabled/%s" % env.app_url 
    if exists(destination_link):
        sudo("rm %s" % destination_link)
    sudo('ln -s /etc/nginx/sites-available/%s /etc/nginx/sites-enabled/' % env.app_url)


def configure_gunicorn_supervisor(context):
    upload_template('./gunicorn-supervisor.template.j2', '/etc/supervisor/conf.d/%s.conf' % env.user, context=context, use_jinja=True, use_sudo=True)
    sudo('supervisorctl reread')
    sudo('supervisorctl update')


def restart_supervisor_nginx():
    sudo('service nginx restart')
    sudo('supervisorctl restart all')
