from abc import ABCMeta

from .environment_state import EnvironmentState


class EnvironmentInterface(EnvironmentState, metaclass=ABCMeta):
    pass
