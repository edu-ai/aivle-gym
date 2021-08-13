import gym

from agent_side_env import AgentEnv
from serializer import CartPoleEnvSerializer


class CartPoleAgentEnv(AgentEnv):
    def __init__(self):
        base_env = gym.make('CartPole-v0')
        super().__init__(CartPoleEnvSerializer(), base_env.action_space, base_env.observation_space,
                         base_env.reward_range)


def main():
    env = CartPoleAgentEnv()
    for i_episode in range(20):
        env.reset()
        for t in range(100):
            env.render()
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)
            if done:
                print("Episode finished after {} timesteps".format(t + 1))
                break
    env.close()


if __name__ == "__main__":
    main()
