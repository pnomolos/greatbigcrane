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
def bootstrap(project_id):
    '''Run the bootstrap process inside the given project's base directory.'''
    print("running bootstrap %s" % project_id)
    project = Project.objects.get(id=project_id)
    process = subprocess.Popen("python bootstrap.py init", cwd=project.base_directory,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    print process.communicate()[0]
    print process.returncode

command_map = {
    'BOOTSTRAP': bootstrap,
}
