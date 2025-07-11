"""The clients that interact with the streaming service APIs."""

import contextlib
import logging
import sys
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

import aiohttp
import aiolimiter

from ..utils.ssl_utils import get_aiohttp_connector_kwargs
from .downloadable import Downloadable

# Type aliases for better readability
HeadersDict = Dict[str, str]
MetadataDict = Dict[str, Any]
SearchResultList = List[Dict[str, Any]]
RateLimiterType = Union[aiolimiter.AsyncLimiter, contextlib.nullcontext[Any]]

logger = logging.getLogger("streamrip")

# Log Python version information
logger.debug("Python version: %s", sys.version)

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"
)


class Client(ABC):
    """Abstract base class for streaming service clients.

    This class defines the interface that all streaming service clients must implement.
    It provides common functionality for authentication, searching, and downloading content.
    """

    source: str
    max_quality: int
    logged_in: bool
    session: aiohttp.ClientSession

    @abstractmethod
    async def login(self) -> None:
        """Log in to the streaming service.

        This method should establish a session and authenticate with the service.
        Subclasses must implement this method.

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        logger.debug(
            "Abstract login method called - this should be implemented by subclasses"
        )
        raise NotImplementedError("login method must be implemented by subclasses")

    @abstractmethod
    async def get_metadata(self, item: str, media_type: str) -> MetadataDict:
        """Get metadata for a specific item.

        Args:
            item: The ID of the item to fetch metadata for
            media_type: The type of media (track, album, etc.)

        Returns:
            A dictionary containing the metadata

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        logger.debug(
            "Abstract get_metadata method called - this should be implemented by subclasses"
        )
        raise NotImplementedError(
            "get_metadata method must be implemented by subclasses"
        )

    @abstractmethod
    async def search(
        self, media_type: str, query: str, limit: int = 500
    ) -> SearchResultList:
        """Search for items matching the query.

        Args:
            media_type: The type of media to search for
            query: The search query
            limit: Maximum number of results to return

        Returns:
            A list of dictionaries containing search results

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        logger.debug(
            "Abstract search method called - this should be implemented by subclasses"
        )
        raise NotImplementedError("search method must be implemented by subclasses")

    @abstractmethod
    async def get_downloadable(self, item: str, quality: int) -> Downloadable:
        """Get a downloadable object for a specific item.

        Args:
            item: The ID of the item to download
            quality: The quality to download at

        Returns:
            A Downloadable object
        """
        logger.debug(
            "Abstract get_downloadable method called - this should be implemented by subclasses"
        )
        raise NotImplementedError(
            "get_downloadable method must be implemented by subclasses"
        )

    @staticmethod
    def get_rate_limiter(requests_per_min: int) -> RateLimiterType:
        """Get a rate limiter for API requests.

        Args:
            requests_per_min: Maximum number of requests per minute (0 for no limit)

        Returns:
            An AsyncLimiter if requests_per_min > 0, otherwise a nullcontext
        """
        if requests_per_min > 0:
            return aiolimiter.AsyncLimiter(requests_per_min, 60)
        else:
            return contextlib.nullcontext()

    @staticmethod
    async def get_session(
        headers: Optional[HeadersDict] = None, verify_ssl: bool = True
    ) -> aiohttp.ClientSession:
        """Create an aiohttp ClientSession with appropriate settings.

        Args:
            headers: Optional headers to include in requests
            verify_ssl: Whether to verify SSL certificates

        Returns:
            An initialized aiohttp.ClientSession
        """
        if headers is None:
            headers = {}

        # Add detailed logging for debugging
        logger.debug("Creating session with verify_ssl=%s", verify_ssl)

        # Get connector kwargs based on SSL verification setting
        connector_kwargs = get_aiohttp_connector_kwargs(verify_ssl=verify_ssl)
        logger.debug(
            "Connector kwargs type: %s, value: %s",
            type(connector_kwargs),
            connector_kwargs,
        )

        # Create connector with explicit parameters instead of unpacking
        if not verify_ssl:
            logger.debug("Creating connector with SSL verification disabled")
            connector = aiohttp.TCPConnector(verify_ssl=False)
        elif "ssl" in connector_kwargs:
            logger.debug("Creating connector with custom SSL context")
            connector = aiohttp.TCPConnector(ssl=connector_kwargs["ssl"])
        else:
            logger.debug("Creating connector with default SSL verification")
            connector = aiohttp.TCPConnector(verify_ssl=True)

        # Use dict.update instead of pipe operator for compatibility
        user_agent_header: HeadersDict = {"User-Agent": DEFAULT_USER_AGENT}
        if headers:
            user_agent_header.update(headers)

        logger.debug("Creating ClientSession with headers: %s", user_agent_header)
        return aiohttp.ClientSession(
            headers=user_agent_header,
            connector=connector,
        )
