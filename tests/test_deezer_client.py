import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from streamrip.client.deezer import DeezerClient
from streamrip.config import Config
from streamrip.exceptions import AuthenticationError, MissingCredentialsError

from util import arun


@pytest.fixture
def deezer_client():
    with patch("deezer.Deezer") as mock_deezer:
        config = Config.defaults()
        client = DeezerClient(config)
        client.client = mock_deezer
        yield client


def test_deezer_login_success(deezer_client):
    deezer_client.config.arl = "test_arl"
    deezer_client.client.login_via_arl.return_value = True

    arun(deezer_client.login())

    deezer_client.client.login_via_arl.assert_called_once_with("test_arl")
    assert deezer_client.logged_in is True


def test_deezer_login_missing_credentials(deezer_client):
    deezer_client.config.arl = None
    with pytest.raises(MissingCredentialsError):
        arun(deezer_client.login())


def test_deezer_login_failure(deezer_client):
    deezer_client.config.arl = "test_arl"
    deezer_client.client.login_via_arl.return_value = False
    with pytest.raises(AuthenticationError):
        arun(deezer_client.login())


def test_get_metadata_track(deezer_client):
    fake_track = {
        "id": "12345",
        "title": "Test Track",
        "album": {
            "id": "54321",
            "title": "Test Album"
        }
    }
    fake_album = {
        "id": "54321",
        "title": "Test Album",
    }
    fake_album_tracks = {
        "data": [
            {"id": "12345", "title": "Test Track"},
            {"id": "67890", "title": "Another Track"}
        ]
    }

    deezer_client.client.api.get_track.return_value = fake_track
    deezer_client.client.api.get_album.return_value = fake_album
    deezer_client.client.api.get_album_tracks.return_value = fake_album_tracks

    result = arun(deezer_client.get_metadata("12345", "track"))

    assert result["title"] == "Test Track"
    assert result["album"]["title"] == "Test Album"
    assert len(result["album"]["tracks"]) == 2
    assert result["album"]["track_total"] == 2
    deezer_client.client.api.get_track.assert_called_once_with("12345")
    deezer_client.client.api.get_album.assert_called_once_with("54321")
    deezer_client.client.api.get_album_tracks.assert_called_once_with("54321")


def test_get_metadata_album(deezer_client):
    fake_album = {
        "id": "54321",
        "title": "Test Album",
    }
    fake_album_tracks = {
        "data": [
            {"id": "12345", "title": "Test Track"},
            {"id": "67890", "title": "Another Track"}
        ]
    }

    deezer_client.client.api.get_album.return_value = fake_album
    deezer_client.client.api.get_album_tracks.return_value = fake_album_tracks

    result = arun(deezer_client.get_metadata("54321", "album"))

    assert result["title"] == "Test Album"
    assert len(result["tracks"]) == 2
    assert result["track_total"] == 2
    deezer_client.client.api.get_album.assert_called_once_with("54321")
    deezer_client.client.api.get_album_tracks.assert_called_once_with("54321")


def test_get_metadata_playlist(deezer_client):
    fake_playlist = {
        "id": "pl123",
        "title": "Test Playlist",
    }
    fake_playlist_tracks = {
        "data": [
            {"id": "12345", "title": "Test Track"},
            {"id": "67890", "title": "Another Track"}
        ]
    }

    deezer_client.client.api.get_playlist.return_value = fake_playlist
    deezer_client.client.api.get_playlist_tracks.return_value = fake_playlist_tracks

    result = arun(deezer_client.get_metadata("pl123", "playlist"))

    assert result["title"] == "Test Playlist"
    assert len(result["tracks"]) == 2
    assert result["track_total"] == 2
    deezer_client.client.api.get_playlist.assert_called_once_with("pl123")
    deezer_client.client.api.get_playlist_tracks.assert_called_once_with("pl123")


def test_get_metadata_artist(deezer_client):
    fake_artist = {
        "id": "art123",
        "name": "Test Artist",
    }
    fake_artist_albums = {
        "data": [
            {"id": "alb1", "title": "Album 1"},
            {"id": "alb2", "title": "Album 2"}
        ]
    }

    deezer_client.client.api.get_artist.return_value = fake_artist
    deezer_client.client.api.get_artist_albums.return_value = fake_artist_albums

    result = arun(deezer_client.get_metadata("art123", "artist"))

    assert result["name"] == "Test Artist"
    assert len(result["albums"]) == 2
    deezer_client.client.api.get_artist.assert_called_once_with("art123")
    deezer_client.client.api.get_artist_albums.assert_called_once_with("art123")


def test_get_metadata_invalid_type(deezer_client):
    with pytest.raises(Exception, match="Media type invalid not available on deezer"):
        arun(deezer_client.get_metadata("123", "invalid"))


def test_search_success(deezer_client):
    mock_search_func = MagicMock()
    mock_search_func.return_value = {
        "data": [{"title": "Test Result"}],
        "total": 1
    }
    deezer_client.client.api.search_album = mock_search_func

    result = arun(deezer_client.search("album", "test query"))

    assert len(result) == 1
    assert result[0]["total"] == 1
    mock_search_func.assert_called_once_with("test query", limit=200)


def test_search_no_results(deezer_client):
    mock_search_func = MagicMock()
    mock_search_func.return_value = {
        "data": [],
        "total": 0
    }
    deezer_client.client.api.search_album = mock_search_func

    result = arun(deezer_client.search("album", "test query"))

    assert len(result) == 0
    mock_search_func.assert_called_once_with("test query", limit=200)


def test_search_invalid_media_type(deezer_client):
    class MockApi:
        pass
    deezer_client.client.api = MockApi()
    with pytest.raises(Exception, match="Invalid media type invalid"):
        arun(deezer_client.search("invalid", "test query"))


def test_search_featured(deezer_client):
    mock_search_func = MagicMock()
    mock_search_func.return_value = {
        "data": [{"title": "Featured Result"}],
        "total": 1
    }
    deezer_client.client.api.get_editorial_releases = mock_search_func

    result = arun(deezer_client.search("featured", ""))

    assert len(result) == 1
    assert result[0]["total"] == 1
    mock_search_func.assert_called_once_with("", limit=200)


def test_search_featured_with_query(deezer_client):
    mock_search_func = MagicMock()
    mock_search_func.return_value = {
        "data": [{"title": "Featured Result"}],
        "total": 1
    }
    deezer_client.client.api.get_editorial_charts = mock_search_func

    result = arun(deezer_client.search("featured", "charts"))

    assert len(result) == 1
    assert result[0]["total"] == 1
    mock_search_func.assert_called_once_with("charts", limit=200)


def test_search_featured_invalid_query(deezer_client):
    class MockApi:
        pass
    deezer_client.client.api = MockApi()
    with pytest.raises(Exception, match='Invalid editorical selection "invalid"'):
        arun(deezer_client.search("featured", "invalid"))
