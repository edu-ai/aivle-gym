import logging
import time
from multiprocessing import Process

from example.agent import CartPoleAgentEnv
from example.judge import CartPoleJudgeEnv


def run_agent():
    env = CartPoleAgentEnv()
    for i_episode in range(2):
        env.reset()
        for t in range(100):
            # time.sleep(0.1)
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)
            if done:
                logging.info("Episode finished after {} timesteps".format(t + 1))
                break
        time.sleep(2)
    env.close()


def main():
    judge_env = CartPoleJudgeEnv()
    judge_proc = Process(target=judge_env.start, args=())
    judge_proc.start()
    agent_proc = Process(target=run_agent, args=())
    agent_proc.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
