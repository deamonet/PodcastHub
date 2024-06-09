from yaml import load

from entity.configuration import Configuration

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open("../application.yml", 'r') as stream:
    CONFIG = Configuration.model_validate(load(stream, Loader=Loader))
    CONFIG.storage.audio = CONFIG.storage.root_path + CONFIG.storage.audio
    CONFIG.storage.video = CONFIG.storage.root_path + CONFIG.storage.video
    CONFIG.storage.episode = CONFIG.storage.root_path + CONFIG.storage.episode
    print(CONFIG)
