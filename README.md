walt
====

a pythonical django approach for adaptation (Wander / Watch, Ask, Learn, Tell)



[install virtualenv, virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)
	cd walt
	pip install -r requirements.txt

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
