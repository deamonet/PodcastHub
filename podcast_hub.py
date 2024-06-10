import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import podcast
from configuration import CONFIG
from update import UPDATE_TASKS

app = FastAPI()
app.mount(CONFIG.storage.static, StaticFiles(directory=CONFIG.storage.audio), name="static")


@app.on_event("startup")
async def lifespan():
    print(app.__dict__)
    scheduler = BackgroundScheduler()
    for update in UPDATE_TASKS:
        update.main_flow()
        scheduler.add_job(update.main_flow, "interval", hours=2)
    podcast.main_flow()
    scheduler.add_job(podcast.main_flow, "interval", hours=2)
    scheduler.start()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/podcast/{name}/{uid}")
async def user_podcast(name: str, uid: int) -> str:
    return podcast.user_podcast(name, uid)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
