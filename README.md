millibank
=========

fork the millibank repositor - we use '/path/to/' as base folder - create a specific virtualenv and activate it;
then, install dependecies from the requirements.txt:
	
	$ cd /path/to/millibank
	$ workon millibank
	(millibank)$ pip install -r requirements.txt

create lacking folders and attribute permissions:

	$ cd /path/to/millibank
	(millibank)$ mkdir sqlite logs

copy local_settings configuration file and modify millibank/local_settings.py according to your own django settings. Cfr. settings.py 
	$ cd /path/to/millibank
	(millibank)$ cp millybank/local_settings.sample.py millybank/local_settings.py 

The local_settings.py stores some basic information about your millibank installation.
These below are the main vars concerning the installation dir and the database backend.
Remaining variables are related to settings.py (feel free to consult the django docs)
	
	MILLIBANK_HOME = "/path/to/millibank"
	MILLIBANK_NAME = "millibank"
	
	DB_BACKEND	= 'django.db.backends.sqlite3'
	DB_NAME	= '%s/sqlite/millibank.db' % MILLIBANK_HOME
	DB_USER = ''
	DB_PASS = ''
	DB_HOST = ''
	DB_PORT	= ''


Mac & Unix installation
Clone the project, we use '/path/to/' as base folder

Create your project virtualenv:

	$ cd /path/to/millybank
	$ mkvirtualenv millybank
	$ pip install -r requirements.txt

… and create the lacking folders (change permissions according to your system configuration)
	
	$ mkdir logs media locale sqlite
	

We added sqlite folder because we will use a sqlite db. Make sure that apache user has the right to write the .db parent folder.

How to compile handlebars templates
---
Frontcast makes use of handlebars templates.
So, firstly install all handlebars requirement for _precompilation. Cfr http://handlebarsjs.com/precompilation.html

	$ cd millybank
	$ handlebars static/js/templates/* -f static/js/walt.handlebars.js

