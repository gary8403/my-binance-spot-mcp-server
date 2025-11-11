"""Trading related API wrapper."""

import logging
from typing import Optional
from .client import BinanceClient

logger = logging.getLogger(__name__)


class Trading:
    """Wrapper for Binance Spot trading APIs."""

    def __init__(self, binance_client: BinanceClient):
        """Initialize Trading wrapper.

        Args:
            binance_client: BinanceClient instance
        """
        self.client = binance_client.get_client()

    def create_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: Optional[float] = None,
        quote_order_qty: Optional[float] = None,
        price: Optional[float] = None,
        time_in_force: Optional[str] = None,
        stop_price: Optional[float] = None,
        iceberg_qty: Optional[float] = None,
        new_client_order_id: Optional[str] = None,
    ) -> dict:
        """Create a new order.

        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            side: Order side - 'BUY' or 'SELL'
            order_type: Order type - 'LIMIT', 'MARKET', 'STOP_LOSS', 'STOP_LOSS_LIMIT',
                       'TAKE_PROFIT', 'TAKE_PROFIT_LIMIT', 'LIMIT_MAKER'
            quantity: Order quantity
            quote_order_qty: Quote order quantity (for MARKET orders)
            price: Order price (required for LIMIT orders)
            time_in_force: Time in force - 'GTC', 'IOC', 'FOK' (required for LIMIT orders)
            stop_price: Stop price (required for STOP orders)
            iceberg_qty: Iceberg quantity for iceberg orders
            new_client_order_id: Custom order ID

        Returns:
            dict: Order creation response

        Raises:
            Exception: If order creation fails
        """
        try:
            params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
            }

            # Add optional parameters
            if quantity is not None:
                params["quantity"] = quantity
            if quote_order_qty is not None:
                params["quoteOrderQty"] = quote_order_qty
            if price is not None:
                params["price"] = price
            if time_in_force is not None:
                params["timeInForce"] = time_in_force
            if stop_price is not None:
                params["stopPrice"] = stop_price
            if iceberg_qty is not None:
                params["icebergQty"] = iceberg_qty
            if new_client_order_id is not None:
                params["newClientOrderId"] = new_client_order_id

            result = self.client.new_order(**params)
            logger.info(f"Order created: {symbol} {side} {order_type}")
            return result
        except Exception as e:
            logger.error(f"Failed to create order for {symbol}: {e}")
            raise

    def test_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: Optional[float] = None,
        quote_order_qty: Optional[float] = None,
        price: Optional[float] = None,
        time_in_force: Optional[str] = None,
    ) -> dict:
        """Test order creation without actually placing the order.

        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            side: Order side - 'BUY' or 'SELL'
            order_type: Order type - 'LIMIT', 'MARKET'
            quantity: Order quantity
            quote_order_qty: Quote order quantity (for MARKET orders)
            price: Order price (required for LIMIT orders)
            time_in_force: Time in force - 'GTC', 'IOC', 'FOK'

        Returns:
            dict: Empty dict if validation passes

        Raises:
            Exception: If order validation fails
        """
        try:
            params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
            }

            if quantity is not None:
                params["quantity"] = quantity
            if quote_order_qty is not None:
                params["quoteOrderQty"] = quote_order_qty
            if price is not None:
                params["price"] = price
            if time_in_force is not None:
                params["timeInForce"] = time_in_force

            result = self.client.new_order_test(**params)
            logger.info(f"Test order validated: {symbol} {side} {order_type}")
            return result
        except Exception as e:
            logger.error(f"Test order validation failed for {symbol}: {e}")
            raise

    def cancel_order(
        self,
        symbol: str,
        order_id: Optional[int] = None,
        orig_client_order_id: Optional[str] = None,
    ) -> dict:
        """Cancel an active order.

        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            order_id: Order ID (either order_id or orig_client_order_id is required)
            orig_client_order_id: Original client order ID

        Returns:
            dict: Cancellation response

        Raises:
            Exception: If cancellation fails
        """
        try:
            params = {"symbol": symbol}

            if order_id is not None:
                params["orderId"] = order_id
            if orig_client_order_id is not None:
                params["origClientOrderId"] = orig_client_order_id

            result = self.client.cancel_order(**params)
            logger.info(f"Order cancelled: {symbol} orderId={order_id}")
            return result
        except Exception as e:
            logger.error(f"Failed to cancel order for {symbol}: {e}")
            raise

    def get_order(
        self,
        symbol: str,
        order_id: Optional[int] = None,
        orig_client_order_id: Optional[str] = None,
    ) -> dict:
        """Check an order's status.

        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            order_id: Order ID (either order_id or orig_client_order_id is required)
            orig_client_order_id: Original client order ID

        Returns:
            dict: Order information

        Raises:
            Exception: If query fails
        """
        try:
            params = {"symbol": symbol}

            if order_id is not None:
                params["orderId"] = order_id
            if orig_client_order_id is not None:
                params["origClientOrderId"] = orig_client_order_id

            result = self.client.get_order(**params)
            logger.debug(f"Retrieved order status for {symbol}: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to get order for {symbol}: {e}")
            raise
