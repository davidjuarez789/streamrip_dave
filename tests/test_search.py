from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from streamrip.rip.search import Searcher


@pytest.mark.asyncio
async def test_searcher_take_first():
    mock_main = MagicMock()
    mock_main.get_logged_in_client = AsyncMock()
    mock_main.add_by_id = AsyncMock()

    mock_client = AsyncMock()
    mock_client.search.return_value = [{"items": [{"id": "123", "title": "test"}]}]
    mock_main.get_logged_in_client.return_value = mock_client

    mock_search_result_item = MagicMock()
    mock_search_result_item.id = "123"
    mock_search_result_item.media_type.return_value = "track"

    mock_search_results = MagicMock()
    mock_search_results.results = [mock_search_result_item]

    with patch("streamrip.rip.search.SearchResults.from_pages", return_value=mock_search_results):
        searcher = Searcher(mock_main)
        await searcher.search_take_first("qobuz", "track", "test")

    mock_main.add_by_id.assert_called_once_with("qobuz", "track", "123")
