import abc
import json
import logging

import zmq

from aivle_gym.env_serializer import EnvSerializer
from aivle_gym.judge_env_base import JudgeEnvBase


class JudgeEnv(JudgeEnvBase, metaclass=abc.ABCMeta):
    # Set this in SOME subclasses
    metadata = {'render.modes': []}
    spec = None

    def __init__(self, serializer: EnvSerializer, action_space, observation_space, reward_range, port: int = 5555):
        super().__init__(serializer, action_space, observation_space, reward_range, port)
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind(f"tcp://*:{self.port}")

    def start(self):
        while True:
            message = self.socket.recv_string()
            req = json.loads(message)
            if req["method"] == "step":
                action = self.serializer.json_to_action(req["action"])
                obs, reward, done, info = self.step(action)
                resp = {
                    "observation": self.serializer.observation_to_json(obs),
                    "reward": reward,
                    "done": done,
                    "info": self.serializer.info_to_json(info)
                }
                self.socket.send_string(json.dumps(resp))
            elif req["method"] == "reset":
                obs = self.reset()
                self.socket.send_string(json.dumps({
                    "accepted": True,
                    "observation": self.serializer.observation_to_json(obs)
                }))
            else:
                pass
            logging.debug(f"Received request from {req['uid']}: {json.loads(message)}")
