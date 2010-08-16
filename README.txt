Zeromq is a dependency of this project. Install it with your favourite package
manager (pacman, brew, etc) or by hand from
http://www.zeromq.org/area:download.  A simple ./configure && make && make
install is sufficient to install it.

Then, to set up Great Big Crane run these commands:

* git clone http://github.com/pnomolos/Django-Dash-2010.git
* cd Django-Dash-2010
* python bootstrap.py
* bin/buildout
* bin/django syncdb
* bin/django migrate

There are three processes that need to be running.  Each one is run from inside
the buildout directory:

* bin/django job_server # Can run multiples of these for more responsivity
* bin/django job_processor
* bin/django runserver

Now visit http://localhost:8000/ and enjoy! Read the about page for a tutorial on
most of the features.

Example test git repos:
git://github.com/xentac/fakezopetestrunner.git
git://github.com/pnomolos/Django-Dash-2010.git <--- Self hosting! Yeah baby!
http://github.com/edorian/Build-your-own-Textadventure.git
http://github.com/jacobian/django-shorturls.git <--- Example of broken tests
