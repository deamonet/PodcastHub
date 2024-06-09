from dataclasses import dataclass


@dataclass
class PodcastEpisode:
    title: str
    pubDate: str
    image: str
    duration: str
    url: str
    length: str
    type: str

    def __init__(self):
        pass


@dataclass
class Podcast:
    author: str
    category: str
    title: str
    link: str
    description: str
    image: str
    episodes: list[PodcastEpisode]

    def __init__(self):
        pass
