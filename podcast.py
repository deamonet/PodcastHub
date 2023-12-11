from dataclasses import dataclass


@dataclass
class Podcast:
    author: str
    category: str
    title: str
    link: str
    description: str
    image: str
    episodes: list[object]


@dataclass
class PodcastEpisode:
    title: str
    pubDate: str
    image: str
    duration: str
    url: str
    length: str
    type: str
