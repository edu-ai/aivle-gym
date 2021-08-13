import gym

from aivle_gym.judge_env import JudgeEnv
from serializer import CartPoleEnvSerializer


class CartPoleJudgeEnv(JudgeEnv):
    def __init__(self):
        super().__init__(CartPoleEnvSerializer())
        self.env = gym.make('CartPole-v0')
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space
        self.reward_range = self.env.reward_range

    def step(self, action):
        return self.env.step(action)

    def reset(self):
        return self.env.reset()

    def render(self, mode='human'):
        return self.env.render(mode=mode)


def main():
    env = CartPoleJudgeEnv()
    env.start()


if __name__ == "__main__":
    main()
