import logging
import time

import gym

from aivle_gym.agent_env import AgentEnv
from judge import CartPoleEnvSerializer


class CartPoleAgentEnv(AgentEnv):
    def __init__(self):
        base_env = gym.make('CartPole-v0')
        super().__init__(CartPoleEnvSerializer(), base_env.action_space, base_env.observation_space,
                         base_env.reward_range, uid=0)


def main():
    env = CartPoleAgentEnv()
    for i_episode in range(10):
        env.reset()
        for t in range(100):
            env.render()
            time.sleep(0.1)
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)
            if done:
                logging.info("Episode finished after {} timesteps".format(t + 1))
                break
        time.sleep(2)
    env.close()


if __name__ == "__main__":
    main()
