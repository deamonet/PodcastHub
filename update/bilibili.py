import re

from configuration import CONFIG
from update.abstract_update import Update


class BilibiliUpdate(Update):
    def __int__(self):
        self.name = 'bilibili'
        self.listen = CONFIG.listen[self.name]
        self.route = self.listen.route
        self.video_prefix_url = self.listen.video_prefix_url
        self.user = self.listen.user

    def extract_video_url(self, dynamic_content: str):
        regex_pattern = "视频地址：<a href=['\"](.*?)['\"]>(.*?)</a>"
        ls = re.findall(regex_pattern, dynamic_content)
        if len(ls) > 0:
            return set(ls[0])
        else:
            return set()


if __name__ == '__main__':
    update = BilibiliUpdate()
    update.main_flow()
