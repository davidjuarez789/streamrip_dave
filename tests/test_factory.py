import pytest

from streamrip.media.factory import create_pending_item
from streamrip.media.pending.album import PendingAlbum
from streamrip.media.pending.artist import PendingArtist
from streamrip.media.pending.label import PendingLabel
from streamrip.media.pending.playlist import PendingPlaylist
from streamrip.media.pending.track import PendingSingle


def test_create_pending_item_album():
    item = create_pending_item("album", "123", None, None, None)
    assert isinstance(item, PendingAlbum)


def test_create_pending_item_track():
    item = create_pending_item("track", "123", None, None, None)
    assert isinstance(item, PendingSingle)


def test_create_pending_item_playlist():
    item = create_pending_item("playlist", "123", None, None, None)
    assert isinstance(item, PendingPlaylist)


def test_create_pending_item_artist():
    item = create_pending_item("artist", "123", None, None, None)
    assert isinstance(item, PendingArtist)


def test_create_pending_item_label():
    item = create_pending_item("label", "123", None, None, None)
    assert isinstance(item, PendingLabel)


def test_create_pending_item_invalid():
    with pytest.raises(ValueError):
        create_pending_item("invalid", "123", None, None, None)
