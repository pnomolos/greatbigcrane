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
