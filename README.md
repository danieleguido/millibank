millibank
=========

fork the millibank repositor - we use '/path/to/' as base folder - create a specific virtualenv and activate it;
then, install dependecies from the requirements.txt:
	
	$ cd /path/to/millibank
	$ workon millibank
	(millibank)$ pip install -r requirements.txt

create lacking folders and attribute permissions:

	(millibank)$ cd /path/to/millibank
	(millibank)$ mkdir sqlite logs locale media

copy local_settings configuration file and modify millibank/local_settings.py according to your own django settings. Cfr. settings.py 
	(millibank)$ cd /path/to/millibank
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

Note that we will use a sqlite db: if you do the same, make sure that apache or wsgi user
has the right to write both the millibank.db file AND millibank.db parent folder.

Finish the installation by doing:

	(millibank)$ cd /path/to/millibank
	(millibank)$ python manage.py syncdb

Then, start the django default dev server to test thath everything is ok, then point your browser to http://127.0.0.1:8000/

	(millibank)$ python manage.py runserver
	Validating models...

	0 errors found
	November 10, 2013 - 20:06:17
	Django version 1.5.4, using settings 'millibank.settings'
	Development server is running at http://127.0.0.1:8000/
	Quit the server with CONTROL-C.
	
That's it for the basic installation!


How to compile handlebars templates
---
Frontcast makes use of handlebars templates.
So, firstly install all handlebars requirement for _precompilation. Cfr http://handlebarsjs.com/precompilation.html

	$ cd millybank
	$ handlebars static/js/templates/* -f static/js/walt.handlebars.js

