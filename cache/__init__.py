import json

from redis import Redis
from configuration import CONFIG
from entity.queue_task import QueueTask, construct

redis_client = Redis(host='omv.local', port=6379, db=0)
BYTE = b'1'
DELIMITER = ":"


def is_queued(task: QueueTask) -> bool:
    return redis_client.exists(DELIMITER.join([CONFIG.cache.is_queued, task.name, task.identifier]))


def queue_in(task: QueueTask):
    if is_queued(task):
        return
    redis_client.set(DELIMITER.join([CONFIG.cache.is_queued, task.name, task.identifier]), 1,
                     ex=CONFIG.cache.expire_seconds)
    redis_client.rpush(CONFIG.cache.task_queue, json.dumps(task.__dict__))


def queue_out():
    task = redis_client.blpop(CONFIG.cache.task_queue)
    task = task[1]
    return construct(json.loads(task.decode("utf-8")))


def queue_clear():
    for key in redis_client.keys(CONFIG.cache.is_queued + "*"):
        redis_client.delete(key)

    redis_client.delete(CONFIG.cache.task_queue)


if __name__ == "__main__":
    queue_clear()
    result = queue_out()
    print(result)
