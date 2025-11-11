"""Order management related API wrapper."""

import logging
from typing import Optional, List
from .client import BinanceClient

logger = logging.getLogger(__name__)


class OrderManagement:
    """Wrapper for Binance Spot order management APIs."""

    def __init__(self, binance_client: BinanceClient):
        """Initialize OrderManagement wrapper.

        Args:
            binance_client: BinanceClient instance
        """
        self.client = binance_client.get_client()

    def get_open_orders(self, symbol: Optional[str] = None) -> List:
        """Get all open orders.

        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT'). If None, returns all symbols.

        Returns:
            list: List of open orders

        Raises:
            Exception: If API request fails
        """
        try:
            if symbol:
                result = self.client.get_open_orders(symbol=symbol)
            else:
                result = self.client.get_open_orders()
            logger.debug(f"Retrieved {len(result)} open orders for {symbol or 'all symbols'}")
            return result
        except Exception as e:
            logger.error(f"Failed to get open orders: {e}")
            raise

    def get_all_orders(
        self,
        symbol: str,
        order_id: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 500,
    ) -> List:
        """Get all orders (active, canceled, filled).

        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            order_id: Order ID to fetch orders from (optional)
            start_time: Start time in milliseconds (optional)
            end_time: End time in milliseconds (optional)
            limit: Number of orders (default: 500, max: 1000)

        Returns:
            list: List of all orders

        Raises:
            Exception: If API request fails
        """
        try:
            params = {"symbol": symbol, "limit": limit}

            if order_id is not None:
                params["orderId"] = order_id
            if start_time is not None:
                params["startTime"] = start_time
            if end_time is not None:
                params["endTime"] = end_time

            result = self.client.get_orders(**params)
            logger.debug(f"Retrieved {len(result)} orders for {symbol}")
            return result
        except Exception as e:
            logger.error(f"Failed to get all orders for {symbol}: {e}")
            raise

    def cancel_all_orders(self, symbol: str) -> List:
        """Cancel all open orders on a symbol.

        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')

        Returns:
            list: List of cancelled orders

        Raises:
            Exception: If cancellation fails
        """
        try:
            result = self.client.cancel_open_orders(symbol=symbol)
            logger.info(f"Cancelled all open orders for {symbol}")
            return result
        except Exception as e:
            logger.error(f"Failed to cancel all orders for {symbol}: {e}")
            raise

    def cancel_open_orders(self, symbol: str) -> List:
        """Cancel all open orders on a symbol (alias for cancel_all_orders).

        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')

        Returns:
            list: List of cancelled orders

        Raises:
            Exception: If cancellation fails
        """
        return self.cancel_all_orders(symbol)

    def get_order_count(self) -> dict:
        """Get current order count usage for all intervals.

        Returns:
            dict: Order count limits and usage

        Raises:
            Exception: If API request fails
        """
        try:
            # Note: This endpoint may not be available in binance-connector
            # It's part of the rate limits info
            result = self.client.get_order_rate_limit()
            logger.debug("Retrieved order count usage")
            return result
        except AttributeError:
            # Fallback if method doesn't exist
            logger.warning("Order rate limit endpoint not available in SDK")
            return {"message": "Order rate limit endpoint not available"}
        except Exception as e:
            logger.error(f"Failed to get order count: {e}")
            raise
