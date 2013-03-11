walt
====

Walt is a lippmanian platform meant to collect papers, video, blogpost like a bookmarker and to
bind them together in series (or protocols) in order to provide augmented documentation and pseudo-scenario for 
web documentary purposes.

Walt is basically a django python project.

---

Mac & Unix installation
---
Note: we use '/path/to/' as base folder

git init walt
	$ cd /path/to
	$ git clone git@github.com:danieleguido/walt.git

Then [install virtualenv, virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)

	$ pip install virtualenvwrapper
	...
	$ export WORKON_HOME=~/Envs
	$ mkdir -p $WORKON_HOME
	$ source /usr/local/bin/virtualenvwrapper.sh
	
Create your walt virtualenv:
	
	$ mkvirtualenv walt
	$ cd walt
	$ pip install -r requirements.txt

… and create the lacking folders (change permission according to your system configuration)

	$ mkdir logs media locale sqlite
	
We added sqlite folder because we will use a sqlite db. Make sure that apache user has the right to write the .db parent folder.


Copy `walt/local_settings.py.sample` to `walt/local_settings.py` and change it according to your LOCAL configuration (cfr `walt/settings.py`). This file is gitignored.

Configure apache conf and your wsgi. We provide to sample file as well.

Create admin link,
	
	$ cd /path/to/walt/static/
	$ ln -s /path/to/Envs/walt/lib/python2.6/site-packages/django/contrib/admin/static/admin admin

and do a proper syncdb command
	
	$ cd /path/to/walt/
	$ python manage.py syncdb
	
finally, runserver (test environment)

	$ python manage.py runserver

point your browser your local [setup page](http://127.0.0.1:8000/setup/)
 - our is http://127.0.0.1:8000/setup/, then back to http://127.0.0.1:8000/
 
 you should see 4 columns named Wander, Ask, Learn and Try respectively.
 
 ___
 
 Notes
 ---
 
 Thanks to adapt.js we have a fluid and flexible 960grid.
 Adapt css modification (added to the end):
 
 
 	.grid_12.floating{position:absolute;margin-left:-470px;left:50%;}
 
	
