import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import podcast
from configuration import CONFIG
from update import Update

app = FastAPI()
app.mount(CONFIG.storage.static, StaticFiles(directory=CONFIG.storage.audio), name="static")


@app.on_event("startup")
def lifespan():
    print(app.__dict__)
    scheduler = BackgroundScheduler()
    for update_class in Update.__subclasses__():
        print(update_class.__name__)
        update = update_class()
        scheduler.add_job(update.main_flow, "interval", hours=2)

    scheduler.add_job(podcast.main_flow, "interval", minutes=1)
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
    uvicorn.run(app, host="0.0.0.0", port=CONFIG.server.port)
