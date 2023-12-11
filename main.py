from fastapi import FastAPI

from source.bilibili import BiliPodcast

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
    return BiliPodcast.podcast(uid)