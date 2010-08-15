Zeromq is a dependency of this project.  It must be installed from source or through a package manager (brew, etc).


The job server and at least one job processor work need to be running for greatbigcrane to run. Try this for testing: 

* Open a terminal and run bin/django job_server
* Open another terminal and run bin/django job_processor
* Open another terminal and run bin/django runserver

Example test git repos:
http://github.com/xentac/fakezopetestrunner
http://github.com/pnomolos/Django-Dash-2010 <--- Self hosting! Yeah baby!
