import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

from streamrip.exceptions import NonStreamableError

from ...client import Client
from ...config import Config
from ...db import Database
from ...metadata import LabelMetadata
from ..media import Pending
from .album import PendingAlbum

if TYPE_CHECKING:
    from ..label import Label


logger = logging.getLogger(__name__)


@dataclass(slots=True)
class PendingLabel(Pending):
    id: str
    client: Client
    config: Config
    db: Database

    async def resolve(self) -> "Label | None":
        try:
            resp = await self.client.get_metadata(self.id, "label")
        except NonStreamableError as e:
            logger.error(f"Error resolving Label: {e}")
            return None
        try:
            meta = LabelMetadata.from_resp(resp, self.client.source)
        except Exception as e:
            logger.error(f"Error resolving Label: {e}")
            return None
        albums = [
            PendingAlbum(album_id, self.client, self.config, self.db)
            for album_id in meta.album_ids()
        ]
        from ..label import Label
        return Label(meta.name, albums, self.client, self.config)
