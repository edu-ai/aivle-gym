import logging
import sys
import time

import gym
import ma_gym

from aivle_gym.agent_env import AgentEnv
from multi_judge import PongEnvSerializer


class PongAgentEnv(AgentEnv):
    def __init__(self, uid):
        base_env = gym.make("PongDuel-v0")
        super().__init__(PongEnvSerializer(), base_env.action_space[0], base_env.observation_space[0],
                         base_env.reward_range, uid=uid)


def main():
    # print(sys.argv[0])
    env = PongAgentEnv(uid=int(sys.argv[1]))
    for _ in range(5):
        env.reset()
        for t in range(1000):
            action = env.action_space.sample()
            obs, reward, done, info = env.step(action)
            time.sleep(0.05)
            logging.debug(f"{action}-{obs}-{reward}-{done}-{info}")
            if done:
                break
    env.close()


if __name__ == "__main__":
    main()
