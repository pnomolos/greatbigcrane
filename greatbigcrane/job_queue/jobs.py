import zmq
import json
from job_queue.management.commands.job_processor import command_map

addr = 'tcp://127.0.0.1:5555'

# FIXME: I have no idea if this is threadsafe
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(addr)

def run_job(command, **kwargs):
    '''Run the given command on the job queue, passing it any arguments as kwargs.'''
    assert command in command_map
    kwargs.update(command=command)
    serialized = json.dumps(kwargs)
    socket.send(serialized)
    assert socket.recv() == "ACK"
