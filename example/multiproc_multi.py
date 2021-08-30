import logging
import time
from multiprocessing import Process

from example.multi_judge import PongJudgeEnv
from example.multi_agent import PongAgentEnv


def run_agent(uid):
    env = PongAgentEnv(uid=uid)
    for i_episode in range(2):
        env.reset()
        for t in range(10000):
            time.sleep(0.02)
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)
            if done:
                logging.info("Episode finished after {} timesteps".format(t + 1))
                break
        time.sleep(0.5)
    env.close()


def main():
    judge_env = PongJudgeEnv()
    judge_proc = Process(target=judge_env.start, args=())
    judge_proc.start()
    agent_proc_0 = Process(target=run_agent, args=(0,))
    agent_proc_1 = Process(target=run_agent, args=(1,))
    agent_proc_0.start()
    agent_proc_1.start()
    agent_proc_0.join()
    agent_proc_1.join()
    judge_proc.kill()
    judge_env.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
