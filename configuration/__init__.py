from yaml import load

from entity.configuration import Configuration

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open("../application.yml", 'r') as stream:
    CONFIG = Configuration.model_validate(load(stream, Loader=Loader))
    print(CONFIG)
