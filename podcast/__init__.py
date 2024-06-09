import json
import os

from feedgen.feed import FeedGenerator

import cache
from configuration import CONFIG
from constant import AUDIO_EXTENSION
from entity.podcast import Podcast, PodcastEpisode
from podcast import media


def user_podcast(name, uid):
    pass


def construct_podcast(podcast: Podcast) -> str:
    fg = FeedGenerator()
    fg.load_extension('podcast')
    fg.title(podcast.title)
    fg.description(podcast.description)
    fg.image()
    for episode in podcast.episodes:
        fe = fg.add_entry()
        fe.id(episode.url)
        fe.title(episode.title)
        fe.enclosure(episode.url)
        fe.pubDate(episode.pubDate)

    return fg.rss_str()


def main_flow():
    task = cache.queue_out()
    media.download_video(task)
    file_name = media.convert_video_to_audio(task)

    episode = PodcastEpisode()
    episode.url = "/".join([CONFIG.storage.static, task.name, task.identifier, file_name, AUDIO_EXTENSION])
    episode.title = file_name
    episode_folder = "/".join([CONFIG.storage.episode, task.name, task.id])
    os.system(f"mkdir -p {episode_folder}")
    with open(f"{episode_folder}/{file_name}.json", "w", encoding="utf-8") as fi:
        json.dump(episode.__dict__, fi)
