from pydantic import BaseModel


class NetAddress(BaseModel):
    protocol: str
    host: str
    port: int

    @property
    def address(self) -> str:
        return f"{self.protocol}://{self.host}:{self.port}"


class Cache(BaseModel):
    task_queue: str
    is_queued: str
    expire_seconds: int


class User(BaseModel):
    id: str
    title: str | None = None
    author: str | None = None
    category: list[str] | None = None
    image_url: str | None = None
    description: str | None = None


class Listen(BaseModel):
    user: list[User]
    route: str
    video_url_prefix: str


class Storage(BaseModel):
    root_path: str
    video: str
    audio: str
    episode: str
    static: str


class PodcastConfig(BaseModel):
    max_episodes: int | None = None


class Configuration(BaseModel):
    rsshub: NetAddress
    podcast: PodcastConfig
    redis: NetAddress
    cache: Cache
    listen: dict[str, Listen]
    storage: Storage
