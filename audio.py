
import json
import requests as r

@dataclass
class AudioCard:
    title: str
    pubDate: str
    itunes_item_image: str
    itunes_duration: str
    enclosure_url: str
    enclosure_length: str
    enclosure_type: str


def audio_card(card: str):
    card_data = json.loads(card)
    if card_data == None:
        return None

    desc = card_data['desc']
    aid = card_data['aid']
    # bvid = item?.desc?.bvid || item?.desc?.origin?.bvid;
    cid = card_data['cid']
    pic = card_data['pic']
    ctime = card_data['ctime']

    if aid == None:
        return None

    return AudioCard(desc, ctime, pic, '', audio_url, '', 'audio/x-m4a')

def audio_url():
    url_bilibili_video = f"https://api.bilibili.com/x/player/playurl?avid={aid}&cid={cid}&qn=16&otype=json&fourk=1&fnver=0&fnval=4048"
    headers_bilibili_video = {
        "Referer": f"https://space.bilibili.com/{uid}/",
        'Host': 'api.bilibili.com',
        'Origin': 'https://www.bilibili.com',
        'Connection': 'keep-alive'
    },
    response_bilibili_video = json.loads(
        r.get(url_bilibili_video, headers=headers_bilibili_video).content.decode("utf-8"))
    return response_bilibili_video['data']['dash']['audio']['base_url']