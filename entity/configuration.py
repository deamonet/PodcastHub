from pydantic import BaseModel


class NetAddress(BaseModel):
    protocol: str
    host: str
    port: int

    @property
    def address(self) -> str:
        return f"{self.protocol}://{self.host}:{self.port}"


class Queue(BaseModel):
    task_queue: str
    is_queued: str


class Configuration(BaseModel):
    rsshub: NetAddress
    redis: NetAddress
    queue: Queue
    listen: dict[str, list[int]]
