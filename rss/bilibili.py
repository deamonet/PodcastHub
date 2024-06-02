import itertools

from rss_parser import RSSParser

import cache
from configuration import CONFIG
import logging
import requests
import re

from entity.queue import QueueTask

logger = logging.getLogger(__name__)

BILIBILI = 'bilibili'
ROUTE = 'user/dynamic'
VIDEO_URL_PREFIX = "https://www.bilibili.com/video/"


def parse_dynamic(rss: str):
    rss = RSSParser.parse(rss)
    contents = []
    for item in rss.channel.items:
        logger.info(item.content.description.content)
        contents.append(item.content.description.content)

    return contents


def extract_video_url(dynamic_content: str):
    regex_pattern = "视频地址：<a href=['\"](.*?)['\"]>(.*?)</a>"
    ls = re.findall(regex_pattern, dynamic_content)
    if len(ls) > 0:
        return set(ls[0])
    else:
        return set()


def main_flow():
    rsses = []
    for id in CONFIG.listen[BILIBILI]:
        url = f"{CONFIG.rsshub.address}/{BILIBILI}/{ROUTE}/{id}"
        print(url)
        response = requests.get(url)
        if response.ok:
            print(response.text)
            rsses.append(response.text)

    dynamics = itertools.chain.from_iterable([parse_dynamic(rss) for rss in rsses])
    video_urls = itertools.chain.from_iterable([extract_video_url(dynamic) for dynamic in dynamics])
    for url in video_urls:
        print(url)
        cache.queue_in(QueueTask(BILIBILI, url.replace(VIDEO_URL_PREFIX, "")))


if __name__ == '__main__':
    main_flow()
