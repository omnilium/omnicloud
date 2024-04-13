from enum import Enum


class Role(Enum):
    ALL = "all"
    CONTROL_PLANE = "control-plane"
    STORAGE = "storage"
    WORKER = "worker"
