#!/usr/bin/env python3
"""Test script for client.py functionality"""

import asyncio
import logging
import sys

# Set up logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("test_client")


async def test_client_setup():
    """Test basic Client setup and SSL handling"""
    logger.info("Python version: %s", sys.version)

    try:
        from streamrip.client.client import Client

        logger.info("Successfully imported Client class")

        # Test static methods
        logger.info("Testing get_rate_limiter method")
        limiter = Client.get_rate_limiter(10)
        logger.info("Rate limiter: %s", limiter)

        logger.info("Testing get_session method")
        session = await Client.get_session(verify_ssl=True)
        logger.info("Session created: %s", session)
        await session.close()

        # Test with verify_ssl=False
        logger.info("Testing get_session with verify_ssl=False")
        session = await Client.get_session(verify_ssl=False)
        logger.info("Session created with verify_ssl=False: %s", session)
        await session.close()

        # Test with custom headers
        logger.info("Testing get_session with custom headers")
        session = await Client.get_session(headers={"X-Test": "value"})
        logger.info("Session created with custom headers: %s", session)
        await session.close()

    except Exception as e:
        logger.error("Error during client setup: %s", e, exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(test_client_setup())
