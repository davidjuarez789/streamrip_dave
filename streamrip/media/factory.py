from ..client import Client
from ..config import Config
from ..db import Database
from .media import Pending
from .pending.album import PendingAlbum
from .pending.artist import PendingArtist
from .pending.label import PendingLabel
from .pending.playlist import PendingPlaylist
from .pending.track import PendingSingle


def create_pending_item(
    media_type: str, id: str, client: Client, config: Config, database: Database
) -> Pending:
    """Factory function to create a Pending item."""
    if media_type == "track":
        return PendingSingle(id, client, config, database)
    elif media_type == "album":
        return PendingAlbum(id, client, config, database)
    elif media_type == "playlist":
        return PendingPlaylist(id, client, config, database)
    elif media_type == "label":
        return PendingLabel(id, client, config, database)
    elif media_type == "artist":
        return PendingArtist(id, client, config, database)
    else:
        raise ValueError(f"Unknown media type: {media_type}")
