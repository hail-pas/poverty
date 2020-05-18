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
    download_ks_task = 'download_ks_task'
    download_single_ks_task = 'download_single_ks_task'
    download_single_ks_task_v2 = 'download_single_ks_task_v2'
    notify_ks_task = 'notify_ks_task'
    refund_task = 'refund_task'