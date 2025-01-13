"""Pleroma/Akkoma Graph Crawler"""

import asyncio

from csv import DictWriter

from .common import fetch_fediverse_instance_list
from .mastodon_crawler import MastodonActiveUserCrawler, MastodonFederationCrawler

DELAY_BETWEEN_CONSECUTIVE_REQUESTS = 0.2


class PleromaFederationCrawler(MastodonFederationCrawler):
    SOFTWARE = "pleroma"
    INSTANCE_INFO_API = "/api/v1/instance"


class PleromaActiveUserCrawler(MastodonActiveUserCrawler):
    SOFTWARE = "pleroma"
    INSTANCE_INFO_API = "/api/v1/instance"
    MAX_PAGE_SIZE = 40
    MAX_ID_REGEX = r"max_id=([a-zA-Z0-9]+)"


async def launch_pleroma_crawl():
    start_urls = await fetch_fediverse_instance_list("pleroma")
    start_urls += await fetch_fediverse_instance_list("akkoma")
    start_urls = ["poa.st", "spinster.xyz", "fe.disroot.org"]  # FOR DEBUG

    async with PleromaFederationCrawler(start_urls) as crawler:
        await crawler.launch()

    async with PleromaActiveUserCrawler(start_urls) as crawler:
        await crawler.launch()
