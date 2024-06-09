from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import podcast
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler

from configuration import CONFIG
from rss.update import UPDATE_TASKS

app = FastAPI()
app.mount(CONFIG.storage.static, StaticFiles(directory=CONFIG.storage.audio), name="static")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/podcast/{name}/{uid}")
async def podcast(name: str, uid: str) -> str:
    return podcast.user_podcast(name, uid)


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    for update in UPDATE_TASKS:
        scheduler.add_job(update.main_flow, "interval", hours=2)
    scheduler.add_job(podcast.main_flow, "interval", hours=2)
    scheduler.start()
    yield
