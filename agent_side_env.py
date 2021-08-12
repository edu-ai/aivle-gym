import abc
import json
from typing import Tuple, Any

import gym
import zmq


class NotAllowedToReset(Exception):
    pass


class AgentEnv(gym.Env, metaclass=abc.ABCMeta):
    def __init__(self, port=5555):
        assert isinstance(port, int)
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect(f"tcp://localhost:{port}")

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
        self.socket.send_string(json.dumps({
            "method": "step",
            "args": self._action_to_json(action)
        }))
        msg = self.socket.recv_string()
        obs, reward, done, info = self._json_to_ordi(json.loads(msg))
        print(f"obs: {obs}, reward: {reward}, done: {done}, info: {info}")
        return obs, reward, done, info

    def _remote_reset(self) -> Tuple[bool, Any]:
        """Request remote to reset the environment

        Returns: (accepted, observation)
            accepted (bool): whether the reset request is accepted by the remote\n
            observation (object): if accepted, initial observation will be returned
        """
        print(f"requesting to reset")
        self.socket.send_string(json.dumps({
            "method": "reset"
        }))
        msg = self.socket.recv_string()
        obj = json.loads(msg)
        print(f"reset response: {obj}")
        if obj["accepted"]:
            return True, obj["observation"]
        else:
            return False, None

    def _json_to_ordi(self, ordi_json) -> Tuple[Any, float, bool, dict]:
        obs = ordi_json['observation']
        reward = ordi_json['reward']
        done = ordi_json['done']
        info = ordi_json['info']
        return self._json_to_observation(obs), reward, done, self._json_to_info(info)

    @abc.abstractmethod
    def _action_to_json(self, action):
        """Transform action into serializable object (i.e. can be serailized using json.dump())

        :param action:
        :return action_json:
        """
        pass

    @abc.abstractmethod
    def _json_to_action(self, action_json):
        """Transform serializable object into action native to Gym environment

        :param action_json:
        :return action_gym:
        """
        pass

    @abc.abstractmethod
    def _observation_to_json(self, obs):
        """Transform observation into serializable object (i.e. can be serailized using json.dump())

        :param obs:
        :return obs_json:
        """
        pass

    @abc.abstractmethod
    def _json_to_observation(self, obs_json):
        """Transform serializable object into observation native to Gym environment

        :param obs_json:
        :return obs_gym:
        """
        pass

    @abc.abstractmethod
    def _info_to_json(self, info):
        """Transform info into serializable object (i.e. can be serailized using json.dump())

        :param info:
        :return info_json:
        """
        pass

    @abc.abstractmethod
    def _json_to_info(self, info_json):
        """Transform serializable object into info native to Gym environment

        :param info_json:
        :return info_gym:
        """
        pass


class SampleAgentEnv(AgentEnv):
    def _action_to_json(self, action):
        return action

    def _json_to_action(self, action_json):
        return action_json

    def _observation_to_json(self, obs):
        return obs

    def _json_to_observation(self, obs_json):
        return obs_json

    def _info_to_json(self, info):
        return info

    def _json_to_info(self, info_json):
        return info_json


def main():
    env = SampleAgentEnv()
    env.step("A")
    env.reset()


if __name__ == "__main__":
    main()
