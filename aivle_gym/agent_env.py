import json
import logging
from typing import Tuple, Any

import gym
import zmq

from aivle_gym.env_serializer import EnvSerializer


class NotAllowedToReset(Exception):
    pass


class AgentEnv(gym.Env):
    # Set this in SOME subclasses
    metadata = {"render.modes": []}
    spec = None

    def __init__(
            self,
            serializer: EnvSerializer,
            action_space,
            observation_space,
            reward_range,
            uid,
            port,
            env: gym.Env,
    ):
        self.uid = uid
        self.action_space = action_space
        self.observation_space = observation_space
        self.reward_range = reward_range
        self.serializer = serializer
        self.port = port
        assert isinstance(port, int)
        assert isinstance(uid, int)
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect(f"tcp://localhost:{self.port}")

        # For rendering
        self.image = None
        self.window = None
        self.to_render = False
        self.image_size = None
        self.env = env

    # def reset_socket(self):
    #     context = zmq.Context()
    #     self.socket = context.socket(zmq.REQ)
    #     self.socket.connect(f"tcp://localhost:{self.port}")

    def step(self, action):
        return self._remote_step(action)

    def reset(self):
        ok, obs = self._remote_reset()
        print("HERREEEEEEEEEEEEEEE")
        print(obs)
        if ok:
            return obs
        else:
            raise NotAllowedToReset

    def render(self, mode="human") -> Any:
        self._remote_render(mode)

    def close(self) -> None:
        self._remote_close()

    def seed(self, seed=None) -> None:
        self._remote_seed(seed)

    def _remote_step(self, action) -> Tuple[Any, float, bool, dict]:
        """Request remote to take an action

        Args:
            action (object): an action provided by the agent

        Returns: (observation, reward, done, info)
        """
        logging.debug(f"[AgentEnv {self.uid}| _remote_step] action: {action}")
        self.socket.send_string(
            json.dumps(
                {
                    "uid": self.uid,
                    "method": "step",
                    "action": self.serializer.action_to_json(action),
                }
            )
        )
        msg = self.socket.recv_string()
        obs, reward, done, info = self._json_to_ordi(json.loads(msg))
        logging.debug(
            f"[AgentEnv {self.uid}| _remote_step] response obs: {obs}, reward: {reward}, done: {done}, info: {info}"
        )
        return obs, reward, done, info

    def _remote_reset(self) -> Tuple[bool, Any]:
        """Request remote to reset the environment

        Returns: (accepted, observation)
            accepted (bool): whether the reset request is accepted by the remote\n
            observation (object): if accepted, initial observation will be returned
        """
        logging.debug(f"[AgentEnv {self.uid}| _remote_reset] requesting")
        self.socket.send_string(json.dumps({"uid": self.uid, "method": "reset"}))
        msg = self.socket.recv_string()
        obj = json.loads(msg)
        logging.debug(f"[AgentEnv {self.uid}| _remote_reset] response: {obj}")
        if obj["accepted"]:
            return True, self.serializer.json_to_observation(obj["observation"])
        else:
            return False, None

    def _remote_render(self, mode) -> Any:
        # logging.debug(f"[AgentEnv | _remote_render] requesting")
        self.socket.send_string(
            json.dumps({"uid": self.uid, "method": "render", "mode": mode})
        )
        msg = self.socket.recv_string()
        return json.loads(msg)

    def _remote_close(self) -> None:
        logging.debug(f"[AgentEnv {self.uid}| _remote_close] requesting")
        self.socket.send_string(json.dumps({"uid": self.uid, "method": "close"}))
        _ = self.socket.recv_string()

    def _remote_seed(self, seed) -> None:
        logging.debug(f"[AgentEnv {self.uid}| _remote_seed] seed: {seed}")
        self.socket.send_string(
            json.dumps({"uid": self.uid, "method": "seed", "seed": seed})
        )
        _ = self.socket.recv_string()

    def _json_to_ordi(self, ordi_json) -> Tuple[Any, float, bool, dict]:
        obs = ordi_json["observation"]
        reward = ordi_json["reward"]
        done = ordi_json["done"]
        info = ordi_json["info"]
        return (
            self.serializer.json_to_observation(obs),
            reward,
            done,
            self.serializer.json_to_info(info),
        )
