import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...client import Client
from ...config import Config
from ...db import Database
from ...exceptions import NonStreamableError
from ...metadata import ArtistMetadata
from ..media import Pending
from .album import PendingAlbum

if TYPE_CHECKING:
    from ..artist import Artist


logger = logging.getLogger(__name__)


@dataclass(slots=True)
class PendingArtist(Pending):
    id: str
    client: Client
    config: Config
    db: Database

    async def resolve(self) -> "Artist | None":
        try:
            resp = await self.client.get_metadata(self.id, "artist")
        except NonStreamableError as e:
            logger.error(
                f"Artist {self.id} not available to stream on {self.client.source} ({e})",
            )
            return None

        try:
            meta = ArtistMetadata.from_resp(resp, self.client.source)
        except Exception as e:
            logger.error(
                f"Error building artist metadata: {e}",
            )
            return None

        albums = [
            PendingAlbum(album_id, self.client, self.config, self.db)
            for album_id in meta.album_ids()
        ]
        from ..artist import Artist
        return Artist(meta.name, albums, self.client, self.config)
