from enum import Enum


class ArqQueue(str, Enum):
    """
    arq任务队列
    """
    task = 'task'
    timing = 'timing'
    notify = 'notify'


class ArqTask(str, Enum):
    """
    arq任务
    """
    monitor = "monitor"
