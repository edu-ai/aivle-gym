import abc
from aivle_gym.env_serializer import EnvSerializer


class JudgeEnvBase():
    # Set this in SOME subclasses
    metadata = {"render.modes": []}
    spec = None

    def __init__(
            self,
            serializer: EnvSerializer,
            action_space,
            observation_space,
            reward_range,
            port
    ):
        assert port is None or isinstance(port, int)
        assert isinstance(serializer, EnvSerializer)
        self.port = port
        self.serializer = serializer
        self.action_space = action_space
        self.observation_space = observation_space
        self.reward_range = reward_range
        #super().__init__(domain, instance, enforce_action_constraints, debug)

    @abc.abstractmethod
    def bind(self):
        pass

    @abc.abstractmethod
    def start(self):
        pass

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self):
        pass
        #return super().render(to_display=False)

    def close(self):
        pass

    @abc.abstractmethod
    def seed(self, seed=None):
        pass