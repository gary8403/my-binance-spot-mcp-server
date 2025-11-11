"""Market data related API wrapper."""

import logging
from typing import Optional, List
from .client import BinanceClient

logger = logging.getLogger(__name__)


class MarketData:
    """Wrapper for Binance Spot market data APIs."""

    def __init__(self, binance_client: BinanceClient):
        """Initialize MarketData wrapper.

        Args:
            binance_client: BinanceClient instance
        """
        self.client = binance_client.get_client()

    def get_ticker(self, symbol: str) -> dict:
        """Get symbol price ticker.

        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')

        Returns:
            dict: Price ticker information

        Raises:
            Exception: If API request fails
        """
        try:
            result = self.client.ticker_price(symbol=symbol)
            logger.debug(f"Retrieved ticker for {symbol}: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to get ticker for {symbol}: {e}")
            raise

    def get_orderbook(self, symbol: str, limit: int = 100) -> dict:
        """Get order book depth.

        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            limit: Depth limit (default: 100, max: 5000)

        Returns:
            dict: Order book data with bids and asks

        Raises:
            Exception: If API request fails
        """
        try:
            result = self.client.depth(symbol=symbol, limit=limit)
            logger.debug(f"Retrieved orderbook for {symbol} with limit {limit}")
            return result
        except Exception as e:
            logger.error(f"Failed to get orderbook for {symbol}: {e}")
            raise

    def get_klines(
        self,
        symbol: str,
        interval: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 500,
    ) -> List:
        """Get candlestick/kline data.

        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            interval: Kline interval (e.g., '1m', '5m', '1h', '1d')
            start_time: Start time in milliseconds (optional)
            end_time: End time in milliseconds (optional)
            limit: Number of records (default: 500, max: 1000)

        Returns:
            list: List of kline data

        Raises:
            Exception: If API request fails
        """
        try:
            params = {"symbol": symbol, "interval": interval, "limit": limit}
            if start_time:
                params["startTime"] = start_time
            if end_time:
                params["endTime"] = end_time

            result = self.client.klines(**params)
            logger.debug(f"Retrieved {len(result)} klines for {symbol}")
            return result
        except Exception as e:
            logger.error(f"Failed to get klines for {symbol}: {e}")
            raise

    def get_trades(self, symbol: str, limit: int = 500) -> List:
        """Get recent trades.

        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            limit: Number of trades (default: 500, max: 1000)

        Returns:
            list: List of recent trades

        Raises:
            Exception: If API request fails
        """
        try:
            result = self.client.trades(symbol=symbol, limit=limit)
            logger.debug(f"Retrieved {len(result)} trades for {symbol}")
            return result
        except Exception as e:
            logger.error(f"Failed to get trades for {symbol}: {e}")
            raise

    def get_24hr_ticker(self, symbol: Optional[str] = None) -> dict:
        """Get 24hr price change statistics.

        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT'). If None, returns all symbols.

        Returns:
            dict or list: 24hr ticker statistics

        Raises:
            Exception: If API request fails
        """
        try:
            if symbol:
                result = self.client.ticker_24hr(symbol=symbol)
            else:
                result = self.client.ticker_24hr()
            logger.debug(f"Retrieved 24hr ticker for {symbol or 'all symbols'}")
            return result
        except Exception as e:
            logger.error(f"Failed to get 24hr ticker for {symbol}: {e}")
            raise

    def get_avg_price(self, symbol: str) -> dict:
        """Get average price.

        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')

        Returns:
            dict: Average price data

        Raises:
            Exception: If API request fails
        """
        try:
            result = self.client.avg_price(symbol=symbol)
            logger.debug(f"Retrieved average price for {symbol}: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to get average price for {symbol}: {e}")
            raise

    def get_exchange_info(self, symbol: Optional[str] = None) -> dict:
        """Get exchange information.

        Args:
            symbol: Trading pair symbol (optional). If None, returns all symbols.

        Returns:
            dict: Exchange information including trading rules and symbol info

        Raises:
            Exception: If API request fails
        """
        try:
            if symbol:
                result = self.client.exchange_info(symbol=symbol)
            else:
                result = self.client.exchange_info()
            logger.debug(f"Retrieved exchange info for {symbol or 'all symbols'}")
            return result
        except Exception as e:
            logger.error(f"Failed to get exchange info: {e}")
            raise
