import asyncio
import logging
from dataclasses import dataclass

from .. import progress
from ..client import Client
from ..config import Config
from .media import Media
from .pending.playlist import PendingPlaylistTrack

logger = logging.getLogger("streamrip")


@dataclass(slots=True)
class Playlist(Media):
    name: str
    config: Config
    client: Client
    tracks: list[PendingPlaylistTrack]

    async def preprocess(self):
        progress.add_title(self.name)

    async def postprocess(self):
        progress.remove_title(self.name)

    async def download(self):
        track_resolve_chunk_size = 20

        async def _resolve_download(item: PendingPlaylistTrack):
            try:
                track = await item.resolve()
                if track is None:
                    return
                await track.rip()
            except Exception as e:
                logger.error(f"Error downloading track: {e}")

        batches = self.batch(
            [_resolve_download(track) for track in self.tracks],
            track_resolve_chunk_size,
        )

        for batch in batches:
            results = await asyncio.gather(*batch, return_exceptions=True)

            for result in results:
                if isinstance(result, Exception):
                    logger.error(f"Batch processing error: {result}")

    @staticmethod
    def batch(iterable, n=1):
        total = len(iterable)
        for ndx in range(0, total, n):
            yield iterable[ndx : min(ndx + n, total)]
