import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'greatbigcrane.development'
import zmq
import time
import json

addr = 'tcp://127.0.0.1:5555'

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(addr)

def bootstrap(project):
    print("processing %s" % project)

command_map = {
    'BOOTSTRAP': bootstrap,
}

while True:
    socket.send("GET")
    job = socket.recv()
    if job == "EMPTY":
        time.sleep(1)
        continue

    job = json.loads(job)
    command = command_map[job['command']]
    del job['command']
    command(**job)
