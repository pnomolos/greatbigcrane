Zeromq is a dependency of this project.  Install it with your favourite package manager (pacman, brew, etc) or by hand from http://www.zeromq.org/area:download.  A simple ./configure && make && make install is sufficient to install it.

To set up our project run these commands:

* python bootstrap.py
* bin/buildout
* bin/django syncdb
* bin/django migrate

There are three processes that need to be running.  Each one is run from inside the buildout:

* bin/django job_server
* bin/django job_processor
* bin/django runserver

From there, go to http://localhost:8000/ and enjoy!

Example test git repos:
http://github.com/xentac/fakezopetestrunner
http://github.com/pnomolos/Django-Dash-2010 <--- Self hosting! Yeah baby!
http://github.com/edorian/Build-your-own-Textadventure.git
