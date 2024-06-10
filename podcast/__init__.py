import json
import os

from feedgen.feed import FeedGenerator

import cache
from configuration import CONFIG
from constant import AUDIO_EXTENSION
from entity.configuration import User
from entity.podcast import Podcast, PodcastEpisode, construct_episode
from podcast import media


def construct_podcast_episode(name: str, uid: str) -> list[PodcastEpisode]:
    episodes_folder = f"{CONFIG.storage.episode}/{name}/{uid}"
    episodes = []
    counter = 0
    for root, dirs, files in os.walk(episodes_folder):
        for file in files:
            if counter == CONFIG.podcast.max_episodes:
                break

            with open(root + "/" + file, "r") as f:
                json_dict = json.load(f)
                episodes.append(construct_episode(json_dict))

            counter += 1

        break
    return episodes


def construct_podcast(name: str, uid: str, episodes: list[PodcastEpisode]) -> Podcast:
    user = User()
    podcast = Podcast()
    for u in CONFIG.listen[name].user:
        if u.id == uid:
            user = u

    podcast.title = user.title
    podcast.author = user.author
    podcast.description = user.description
    podcast.episodes = episodes
    podcast.category = user.category
    return podcast


def construct_podcast_rss(podcast: Podcast) -> str:
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


def user_podcast(name, uid):
    episodes = construct_podcast_episode(name, uid)
    podcast = construct_podcast(name, uid, episodes)
    return construct_podcast_rss(podcast)


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
