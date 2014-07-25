Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3
* Git
* pip
* virtualenv
* supervisor

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, eg, lekum.org 

## Supervisor conf file

* see gunicorn-supervisor.template.conf
* replace SITENAME with, eg, lekum.org 

## Folder structure:
Assume we have a user account at /home/username

	/home/username
	    └── sites
		└── SITENAME
		    ├── database
		    ├── source
		    ├── static
		    └── virtualenv
