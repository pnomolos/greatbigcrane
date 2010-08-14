import zmq
import Queue

addr = 'tcp://127.0.0.1:5555'

context = zmq.Context()
socket = context.socket(zmq.REP) # Receives job requests from application server
socket.bind(addr)

jobs = Queue.Queue()

print("Job Server Is Running")
while True:
    request = socket.recv()
    socket.send("ACK")
    if request == "GET":
        # Request came from a worker send it the next available job
        try:
            job = jobs.get_nowait()
            socket.send(job)
        except Queue.Empty, e:
            socket.send("EMPTY")
    else:
        # Request came from the django app, queue the job
        jobs.put(request)
