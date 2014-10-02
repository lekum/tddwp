Provisioning a new site
=======================

This instructions are valid for deploying on a Debian remote server.

First, intall python2 and this packages::

    pip install fabric jinja2

Then, run this::

    fab provision_and_deploy:host=debian@dev --set app_url="dev.net"

where ``debian`` is the username that will host the app code, ``dev`` is the hostname and ``app_url`` will be the url to access the application.

To deploy a new version, run just ``fab deploy:host=debian@dev``.
