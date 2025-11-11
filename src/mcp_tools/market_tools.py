"""MCP tools for market data."""

import logging
from typing import Optional
from ..binance_wrapper.market import MarketData

logger = logging.getLogger(__name__)


def register_market_tools(mcp, market_data: MarketData, enabled_tools: list):
    """Register market data tools with MCP server.

    Args:
        mcp: FastMCP server instance
        market_data: MarketData instance
        enabled_tools: List of enabled tool names
    """

    if "get_symbol_ticker" in enabled_tools:

        @mcp.tool()
        def get_symbol_ticker(symbol: str) -> dict:
            """Get symbol price ticker.

            Args:
                symbol: Trading pair symbol (e.g., 'BTCUSDT')

            Returns:
                dict: Price ticker information including symbol and price
            """
            return market_data.get_ticker(symbol)

    if "get_orderbook" in enabled_tools:

        @mcp.tool()
        def get_orderbook(symbol: str, limit: int = 100) -> dict:
            """Get order book depth.

            Args:
                symbol: Trading pair symbol (e.g., 'BTCUSDT')
                limit: Depth limit (default: 100, max: 5000)

            Returns:
                dict: Order book data with bids and asks
            """
            return market_data.get_orderbook(symbol, limit)

    if "get_klines" in enabled_tools:

        @mcp.tool()
        def get_klines(
            symbol: str,
            interval: str,
            start_time: Optional[int] = None,
            end_time: Optional[int] = None,
            limit: int = 500,
        ) -> list:
            """Get candlestick/kline data.

            Args:
                symbol: Trading pair symbol (e.g., 'BTCUSDT')
                interval: Kline interval (e.g., '1m', '5m', '1h', '1d')
                start_time: Start time in milliseconds (optional)
                end_time: End time in milliseconds (optional)
                limit: Number of records (default: 500, max: 1000)

            Returns:
                list: List of kline data [openTime, open, high, low, close, volume, ...]
            """
            return market_data.get_klines(symbol, interval, start_time, end_time, limit)

    if "get_trades" in enabled_tools:

        @mcp.tool()
        def get_trades(symbol: str, limit: int = 500) -> list:
            """Get recent trades.

            Args:
                symbol: Trading pair symbol (e.g., 'BTCUSDT')
                limit: Number of trades (default: 500, max: 1000)

            Returns:
                list: List of recent trades
            """
            return market_data.get_trades(symbol, limit)

    if "get_24hr_ticker" in enabled_tools:

        @mcp.tool()
        def get_24hr_ticker(symbol: Optional[str] = None) -> dict:
            """Get 24hr price change statistics.

            Args:
                symbol: Trading pair symbol (e.g., 'BTCUSDT'). If not provided, returns all symbols.

            Returns:
                dict or list: 24hr ticker statistics
            """
            return market_data.get_24hr_ticker(symbol)

    if "get_avg_price" in enabled_tools:

        @mcp.tool()
        def get_avg_price(symbol: str) -> dict:
            """Get average price.

            Args:
                symbol: Trading pair symbol (e.g., 'BTCUSDT')

            Returns:
                dict: Average price data
            """
            return market_data.get_avg_price(symbol)

    if "get_exchange_info" in enabled_tools:

        @mcp.tool()
        def get_exchange_info(symbol: Optional[str] = None) -> dict:
            """Get exchange information.

            Args:
                symbol: Trading pair symbol (optional). If not provided, returns all symbols.

            Returns:
                dict: Exchange information including trading rules and symbol info
            """
            return market_data.get_exchange_info(symbol)

    logger.info(f"Registered {len(enabled_tools)} market tools")
