walt
====

Walt is a lippmanian platform meant to collect papers, video, blogpost like a bookmarker and to
bind them together in series (or protocols) in order to provide augmented documentation and pseudo-scenario for 
web documentary purposes.

Walt is basically a django python project.


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
	...
	
Create your walt virtualenv:
	
	$ mkvirtualenv walt
	$ cd walt
	$ pip install -r requirements.txt

Let's suppose our WORKON_HOME is /path/to/Envs...

Change your LOCAL local_settings.py (cfr settings.py), there is a sample local settings file you can use as base.

Configure apache conf and your wsgi. We provide to sample file as well.

Create admin link,
	
	$ cd /path/to/walt/static/
	$ ln -s /path/to/Envs/walt/lib/python2.6/site-packages/django/contrib/admin/static/admin admin

and do a proper syncdb command
	
	$ cd /path/to/walt/
	$ python manage.py syncdb
	

goto setup apge
