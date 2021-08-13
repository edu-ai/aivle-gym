import abc
import json
import logging

import gym
import zmq

from aivle_gym.env_serializer import EnvSerializer


class JudgeEnv(gym.Env):
    # Set this in SOME subclasses
    metadata = {'render.modes': []}
    spec = None

    def __init__(self, serializer: EnvSerializer, action_space, observation_space, reward_range, port: int = 5555):
        assert isinstance(port, int)
        assert isinstance(serializer, EnvSerializer)
        self.serializer = serializer
        self.action_space = action_space
        self.observation_space = observation_space
        self.reward_range = reward_range
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind(f"tcp://*:{port}")

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
            logging.debug(f"Received request: {json.loads(message)}")

    @abc.abstractmethod
    def step(self, action):
        pass

    @abc.abstractmethod
    def reset(self):
        pass

    @abc.abstractmethod
    def render(self, mode='human'):
        pass

    def close(self):  # TODO
        pass

    def seed(self, seed=None):  # TODO
        pass
