from rss_parser import RSSParser

from rss.update import logger


def parse(rss: str) -> list[str]:
    rss = RSSParser.parse(rss)
    contents = []
    for item in rss.channel.items:
        logger.info(item.content.description.content)
        contents.append(item.content.description.content)

    return contents
