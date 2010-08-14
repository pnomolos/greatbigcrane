"""
Copyright 2010 Jason Chu, Dusty Phillips, and Phil Schalm

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

"""
Copyright 2010 Jason Chu, Dusty Phillips, and Phil Schalm

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import zmq
import time
import json
import subprocess

from django.core.management.base import NoArgsCommand

addr = 'tcp://127.0.0.1:5555'

class Command(NoArgsCommand):
    help = "Run the 0MQ based job processor. Accepts jobs from the job server and processes them."
    def handle(self, **options):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(addr)

        while True:
            socket.send("GET")
            job = socket.recv()
            if job == "EMPTY":
                time.sleep(1)
                continue

            job = json.loads(job)
            command = command_map[job['command']]
            del job['command']
            try:
                command(**job)
            except Exception, e:
                print e


# Create the actual commands here and keep the command_map below up to date
# FIXME: I feel this should go to it's own module
from project.models import Project
from notifications.models import Notification
def bootstrap(project_id):
    '''Run the bootstrap process inside the given project's base directory.'''
    print("running bootstrap %s" % project_id)
    project = Project.objects.get(id=project_id)
    process = subprocess.Popen("python bootstrap.py init", cwd=project.base_directory,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    response = process.communicate()[0]

    Notification.objects.create(status="success" if not process.returncode else "error",
            summary="Bootstrapping '%s' %s" % (
                project.name, "success" if not process.returncode else "error"),
            message=response)


command_map = {
    'BOOTSTRAP': bootstrap,
}
