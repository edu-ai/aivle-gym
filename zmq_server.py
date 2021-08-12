#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#
import json
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv_string()
    req = json.loads(message)
    if req["method"] == "step":
        dummy_json = {
            "observation": [1, 2, 3],
            "reward": 0.5,
            "done": False,
            "info": "hello world"
        }
        socket.send_string(json.dumps(dummy_json))
    elif req["method"] == "reset":
        socket.send_string(json.dumps({
            "accepted": True,
            "observation": [1, 2, 3]
        }))
    else:
        pass
    print(f"Received request: {json.loads(message)}")