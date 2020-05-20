import abc
from enum import IntEnum


class EnumMixin:
    @classmethod
    @abc.abstractmethod
    def choices(cls):
        raise NotImplementedError


class GeneralStatus(EnumMixin, IntEnum):
    on = 1
    off = 2

    @classmethod
    def choices(cls):
        return {
            cls.on: "开启",
            cls.off: "关闭"
        }
