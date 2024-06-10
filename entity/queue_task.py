from dataclasses import dataclass

from configuration import CONFIG
from util import user_utils


@dataclass
class QueueTask:
    id: int
    name: str
    identifier: str
    prefix: str
    title: str
    category: list[str]
    description: str
    image: str

    def __init__(self, name, identifier, id):
        self.name = name
        self.identifier = identifier
        self.id = id


def construct(json_dict: dict[str, str]):
    task = QueueTask("", "", 0)
    for key, value in json_dict.items():
        setattr(task, key, value)

    listen = CONFIG.listen[task.name]
    task.prefix = listen.video_url_prefix
    user = user_utils.match_user(task.name, task.id)
    task.title = user.title
    task.category = user.category
    task.description = user.description
    task.image = user.image_url
    return task
