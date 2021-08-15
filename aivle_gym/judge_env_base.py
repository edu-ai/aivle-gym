import abc

import gym

from aivle_gym.env_serializer import EnvSerializer


class JudgeEnvBase(gym.Env):
    # Set this in SOME subclasses
    metadata = {'render.modes': []}
    spec = None

    def __init__(self, serializer: EnvSerializer, action_space, observation_space, reward_range, port):
        assert isinstance(port, int)
        assert isinstance(serializer, EnvSerializer)
        self.port = port
        self.serializer = serializer
        self.action_space = action_space
        self.observation_space = observation_space
        self.reward_range = reward_range

    @abc.abstractmethod
    def start(self):
        pass

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