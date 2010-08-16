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

import Queue
import zmq

addr = 'tcp://127.0.0.1:5555'

from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = "Run the 0MQ based job server for greatbigcrane."
    def handle(self, **options):
        context = zmq.Context()
        socket = context.socket(zmq.REP) # Receives job requests from application server
        socket.bind(addr)

        jobs = Queue.Queue()

        print("Job Server Is Running")
        while True:
            request = socket.recv()
            if request == "GET":
                # Request came from a worker send it the next available job
                try:
                    job = jobs.get_nowait()
                    socket.send(job)
                except Queue.Empty:
                    socket.send("EMPTY")
            else:
                # Request came from the django app, queue the job
                jobs.put(request)
                socket.send("ACK")
