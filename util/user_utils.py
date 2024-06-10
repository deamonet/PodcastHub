from configuration import CONFIG
from entity.configuration import User


def match_user(name: str, uid: int) -> User | None:
    users = CONFIG.listen[name].user
    if len(users) == 0:
        return

    for user in users:
        if user.id == uid:
            return user
