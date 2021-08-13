import abc
import json

import gym
import zmq

import serializers


class JudgeEnv(gym.Env):
    # Set this in SOME subclasses
    metadata = {'render.modes': []}
    reward_range = (-float('inf'), float('inf'))
    spec = None

    # Set these in ALL subclasses
    action_space = None
    observation_space = None

    def __init__(self, serializer: serializers.EnvSerializer, port: int = 5555):
        assert isinstance(port, int)
        assert isinstance(serializer, serializers.EnvSerializer)
        self.serializer = serializer
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
            print(f"Received request: {json.loads(message)}")

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


class SampleJudgeEnv(JudgeEnv):
    def step(self, action):
        return [1, 2, 3], 0.5, False, str(action)

    def reset(self):
        return [1, 2, 3]

    def render(self, mode='human'):
        pass


if __name__ == "__main__":
    env = SampleJudgeEnv(serializer=serializers.SampleSerializer())
    env.start()
