import json
from typing import Tuple, Any

import gym
import zmq

import serializers
from serializers import EnvSerializer


class NotAllowedToReset(Exception):
    pass


class AgentEnv(gym.Env):
    def __init__(self, serializer: EnvSerializer, port=5555):
        self.serializer = serializer
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
            "action": self.serializer.action_to_json(action)
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
        return self.serializer.json_to_observation(obs), reward, done, self.serializer.json_to_info(info)


def main():
    env = AgentEnv(serializer=serializers.SampleSerializer())
    env.step("A")
    env.reset()


if __name__ == "__main__":
    main()
