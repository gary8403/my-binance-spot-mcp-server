"""Binance client initialization and management."""

import logging
from typing import Optional
from binance.spot import Spot

logger = logging.getLogger(__name__)


class BinanceClient:
    """Wrapper class for Binance Spot API client."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: Optional[str] = None,
        testnet: bool = False,
        proxy_url: Optional[str] = None,
    ):
        """Initialize Binance client.

        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            base_url: Optional custom base URL for Binance API
            testnet: Whether to use testnet (default: False)
            proxy_url: Optional proxy URL (supports http, https, socks5)
                      Example: http://proxy.example.com:8080
                               socks5://proxy.example.com:1080
                               http://username:password@proxy.example.com:8080
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        self.proxy_url = proxy_url

        # Determine base URL
        if base_url:
            self.base_url = base_url
        elif testnet:
            self.base_url = "https://testnet.binance.vision"
        else:
            self.base_url = "https://api.binance.com"

        # Prepare proxies configuration if proxy_url is provided
        proxies = None
        if proxy_url:
            proxies = {"http": proxy_url, "https": proxy_url}
            logger.info(f"Proxy configured: {proxy_url}")

        # Initialize Binance Spot client
        self.client = Spot(
            api_key=self.api_key,
            api_secret=self.api_secret,
            base_url=self.base_url,
            proxies=proxies,
        )

        logger.info(f"Binance client initialized with base URL: {self.base_url}")

    def get_client(self) -> Spot:
        """Get the underlying Binance Spot client.

        Returns:
            Spot: Binance Spot client instance
        """
        return self.client

    def ping(self) -> dict:
        """Test connectivity to the Binance API.

        Returns:
            dict: Empty dict if successful

        Raises:
            Exception: If connection fails
        """
        try:
            result = self.client.ping()
            logger.info("Binance API ping successful")
            return result
        except Exception as e:
            logger.error(f"Binance API ping failed: {e}")
            raise

    def get_server_time(self) -> dict:
        """Get current server time.

        Returns:
            dict: Server time response

        Raises:
            Exception: If request fails
        """
        try:
            result = self.client.time()
            logger.debug(f"Server time retrieved: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to get server time: {e}")
            raise
