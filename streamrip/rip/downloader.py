import asyncio
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .main import Main


logger = logging.getLogger(__name__)


class Downloader:
    def __init__(self, main: "Main"):
        self.main = main

    async def rip(self):
        """Download all resolved items."""
        results = await asyncio.gather(
            *[item.rip() for item in self.main.media], return_exceptions=True
        )

        failed_items = 0
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Error processing media item: {result}")
                failed_items += 1

        if failed_items > 0:
            total_items = len(self.main.media)
            logger.info(
                f"Download completed with {failed_items} failed items out of {total_items} total items."
            )
