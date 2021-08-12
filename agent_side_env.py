import abc
import json
from typing import Tuple, Any

import gym


class NotAllowedToReset(Exception):
    pass


class AgentEnv(gym.Env, metaclass=abc.ABCMeta):
    def step(self, action):
        return self._remote_step(action)

    def reset(self):
        ok, obs = self._remote_reset()
        if ok:
            return obs
        else:
            raise NotAllowedToReset

    def render(self, mode='human'):
        """render method does nothing in AgentEnv class
        """
        pass

    def _remote_step(self, action) -> Tuple[Any, float, bool, dict]:
        """Request remote to take an action

        Args:
            action (object): an action provided by the agent

        Returns: (observation, reward, done, info)
        """
        print(f"requesting to step with action {action}")
        action_json = self._action_to_json(action)
        dummy_json = {
            "observation": [1, 2, 3],
            "reward": 0.5,
            "done": False,
            "info": "hello world"
        }
        return self._json_to_ordi(json.dumps(dummy_json))

    def _remote_reset(self) -> Tuple[bool, Any]:
        """Request remote to reset the environment

        Returns: (accepted, observation)
            accepted (bool): whether the reset request is accepted by the remote\n
            observation (object): if accepted, initial observation will be returned
        """
        print("requesting to reset...")
        return False, None

    def _json_to_ordi(self, ordi_json) -> Tuple[Any, float, bool, dict]:
        ordi = json.loads(ordi_json)
        obs = ordi['observation']
        reward = ordi['reward']
        done = ordi['done']
        info = ordi['info']
        return self._json_to_observation(obs), reward, done, self._json_to_info(info)

    @abc.abstractmethod
    def _action_to_json(self, action):
        pass

    @abc.abstractmethod
    def _json_to_action(self, action_json):
        pass

    @abc.abstractmethod
    def _observation_to_json(self, obs):
        pass

    @abc.abstractmethod
    def _json_to_observation(self, obs_json):
        pass

    @abc.abstractmethod
    def _info_to_json(self, info):
        pass

    @abc.abstractmethod
    def _json_to_info(self, info_json):
        pass


class SampleAgentEnv(AgentEnv):
    def _action_to_json(self, action):
        return json.dumps(action)

    def _json_to_action(self, action_json):
        return action_json

    def _observation_to_json(self, obs):
        return json.dumps(obs)

    def _json_to_observation(self, obs_json):
        return obs_json

    def _info_to_json(self, info):
        return json.dumps(info)

    def _json_to_info(self, info_json):
        return info_json


def main():
    env = SampleAgentEnv()
    env.step("action A")


if __name__ == "__main__":
    main()
