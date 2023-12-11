import json

import requests as r

from podcast import PodcastEpisode, Podcast





class BiliPodcast:

    def __init__(self):
        pass

    @staticmethod
    def podcast(uid: int):
        cards = BiliPodcast.dynamic_cards(uid)
        episodes = []
        link = f"https://space.bilibili.com/{uid}/video"
        for card in cards:
            try:
                title, aid, pic, cid, ctime = BiliPodcast.audio_card(card['card'])
                if title is None:
                    continue

                audio_url = BiliPodcast.audio_url(uid, aid, cid)
                episodes.append(PodcastEpisode(title, ctime, pic, '', audio_url, '', 'audio/x-m4a'))
            except Exception as exception:
                print(exception.args)
                print(exception)
                continue

        image = ''
        author = ''
        title = ''
        category = ''
        description = ''
        return Podcast(author, category, title, link, description, image, episodes=episodes)

    @staticmethod
    def dynamic_cards(uid: int):
        url_bilibili_dynamic = f"https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={uid}"
        headers_bilibili_dynamic = {"Referer": f"https://space.bilibili.com/{uid}/"}
        response_bilibili_dynamic = json.loads(
            r.get(url_bilibili_dynamic, headers=headers_bilibili_dynamic).content.decode('utf-8'))
        return response_bilibili_dynamic['data']['cards']

    @staticmethod
    def audio_card(card: str) -> tuple:
        if card is None or len(card) == 0:
            return None, None, None, None, None
        card_data = json.loads(card)
        if 'aid' not in card_data:
            return None, None, None, None, None

        title = card_data['desc']
        aid = card_data['aid']

        # 注释 bvid = item?.desc?.bvid || item?.desc?.origin?.bvid;
        cid = card_data['cid']
        pic = card_data['pic']
        ctime = card_data['ctime']
        return title, aid, pic, cid, ctime

    @staticmethod
    def audio_url(uid: int, aid: str, cid: str):
        url_bilibili_video = f"https://api.bilibili.com/x/player/playurl?avid={aid}&cid={cid}&qn=16&otype=json&fourk=1&fnver=0&fnval=4048"
        headers_bilibili_video = {
            "Referer": f"https://space.bilibili.com/{uid}/",
            'Host': 'api.bilibili.com',
            'Origin': 'https://www.bilibili.com',
            'Connection': 'keep-alive'
        }
        response_bilibili_video = json.loads(
            r.get(url_bilibili_video, headers=headers_bilibili_video).content.decode("utf-8"))
        return response_bilibili_video['data']['dash']['audio'][0]['base_url']
