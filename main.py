from dataclasses import dataclass
from feedgen.feed import FeedGenerator


from fastapi import FastAPI
import requests as r

app = FastAPI()




@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/audio/{fid}")
async def podcast_audio_file(fid: str):
    pass


@app.get("/podcast/bilibili/{uid}")
async def podcast_bilibili(uid: int):
    url_bilibili_dynamic = f"https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={uid}"
    headers_bilibili_dynamic = {"Referer": f"https://space.bilibili.com/{uid}/"}
    response_bilibili_dynamic = json.loads(
        r.get(url_bilibili_dynamic, headers=headers_bilibili_dynamic).content.decode('utf-8'))
    cards = response_bilibili_dynamic['data']['cards']
    audios = map(AudioCard.audio_card, cards)




