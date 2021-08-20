import gym
import numpy

from aivle_gym.env_serializer import EnvSerializer
from aivle_gym.judge_env import JudgeEnv


class CartPoleJudgeEnv(JudgeEnv):
    def __init__(self):
        self.env = gym.make('CartPole-v0')
        super().__init__(CartPoleEnvSerializer(), self.env.action_space, self.env.observation_space,
                         self.env.reward_range)

    def step(self, action):
        return self.env.step(action)

    def reset(self):
        return self.env.reset()

    def render(self, mode='human'):
        return self.env.render(mode=mode)

    def close(self):
        self.env.close()

    def seed(self, seed=None):
        self.env.seed(seed)


class CartPoleEnvSerializer(EnvSerializer):
    def action_to_json(self, action):
        return action

    def json_to_action(self, action_json):
        return action_json

    def observation_to_json(self, obs):
        return obs.tolist()

    def json_to_observation(self, obs_json):
        return numpy.array(obs_json)

    def info_to_json(self, info):
        return info

    def json_to_info(self, info_json):
        return info_json


def main():
    env = CartPoleJudgeEnv()
    env.start()


if __name__ == "__main__":
    main()
