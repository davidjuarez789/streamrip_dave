from unittest.mock import AsyncMock, MagicMock

import pytest

from streamrip.rip.downloader import Downloader


@pytest.mark.asyncio
async def test_downloader_rip():
    mock_main = MagicMock()
    mock_media_success = MagicMock()
    mock_media_success.rip = AsyncMock()

    async def rip_failure_coro():
        raise Exception("test error")

    mock_rip_failure = AsyncMock(side_effect=rip_failure_coro)
    mock_media_failure = MagicMock()
    mock_media_failure.rip = mock_rip_failure

    mock_main.media = [mock_media_success, mock_media_failure]

    downloader = Downloader(mock_main)
    await downloader.rip()

    mock_media_success.rip.assert_called_once()
    mock_rip_failure.assert_called_once()
