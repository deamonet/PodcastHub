import json
from typing import Awaitable

from redis import Redis
from constant import DAY_SECONDS
from configuration import CONFIG
from entity.queue import QueueTask

redis_client = Redis(host='omv.local', port=6379, db=0)
BYTE = b'1'
DELIMITER = ":"


def is_queued(task: QueueTask) -> bool:
    return redis_client.exists(DELIMITER.join([CONFIG.queue.is_queued, task.name, task.identifier]))


def queue_in(task: QueueTask):
    if is_queued(task):
        return
    redis_client.set(DELIMITER.join([CONFIG.queue.is_queued, task.name, task.identifier]), 1, ex=DAY_SECONDS)
    redis_client.rpush(CONFIG.queue.task_queue, json.dumps(task.__dict__))


def queue_out() -> Awaitable[list] | list:
    return redis_client.blpop(CONFIG.queue.task_queue)
