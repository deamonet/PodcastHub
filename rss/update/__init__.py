import itertools
import cache
import logging
import requests

from configuration import CONFIG
from entity.configuration import User
from entity.queue_task import QueueTask
from rss import parse
from rss.update.bilibili import BilibiliUpdate

logger = logging.getLogger(__name__)

UPDATE_TASKS = (BilibiliUpdate())


class Update:
    def __init__(self):
        self.name = ""
        self.listen = ""
        self.route = ""
        self.video_prefix_url = ""
        self.user = ()

    def extract_video_url(self, rss_entry: str) -> set:
        return set()

    def update_one_user(self, user: User):
        rss_list = []
        url = f"{CONFIG.rsshub.address}/{self.name}/{self.route}/{user.id}"
        print(url)
        response = requests.get(url)
        if response.ok:
            print(response.text)
            rss_list.append(response.text)

        dynamics = itertools.chain.from_iterable([parse(rss) for rss in rss_list])
        video_urls = itertools.chain.from_iterable([self.extract_video_url(dynamic) for dynamic in dynamics])
        for url in video_urls:
            print(url)
            cache.queue_in(QueueTask(self.name, url.replace(self.video_prefix_url, ""), user.id))

    def main_flow(self):
        for user in self.user:
            self.update_one_user(user)
