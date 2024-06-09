from dataclasses import dataclass

from configuration import CONFIG


@dataclass
class QueueTask:
    id: str
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
    task = QueueTask("", "", "")
    for key, value in json_dict.items():
        setattr(task, key, value)

    task.prefix = CONFIG.listen[task.name].video_url_prefix
    task.title = CONFIG.listen[task.name].title
    task.category = CONFIG.listen[task.name].category
    task.description = CONFIG.listen[task.name].description
    task.image = CONFIG.listen[task.name].image_url
    return task
