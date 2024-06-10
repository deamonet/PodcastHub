import itertools
import logging
import re

import requests
from rss_parser import RSSParser

import cache
from configuration import CONFIG
from entity.configuration import User
from entity.queue_task import QueueTask

logger = logging.getLogger(__name__)


class Update:
    def __init__(self):
        self.name = ""
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


def parse(rss: str) -> list[str]:
    rss = RSSParser.parse(rss)
    contents = []
    for item in rss.channel.items:
        logger.info(item.content.description.content)
        contents.append(item.content.description.content)

    return contents


class BilibiliUpdate(Update):
    def __init__(self):
        super().__init__()
        self.name = 'bilibili'
        listen = CONFIG.listen[self.name]
        self.route = listen.route
        self.video_prefix_url = listen.video_url_prefix
        self.user = listen.user

    def extract_video_url(self, dynamic_content: str):
        regex_pattern = "视频地址：<a href=['\"](.*?)['\"]>(.*?)</a>"
        ls = re.findall(regex_pattern, dynamic_content)
        if len(ls) > 0:
            return set(ls[0])
        else:
            return set()
