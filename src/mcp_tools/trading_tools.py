"""MCP tools for trading."""

import logging
from typing import Optional
from ..binance_wrapper.trading import Trading

logger = logging.getLogger(__name__)


def register_trading_tools(mcp, trading: Trading, enabled_tools: list):
    """Register trading tools with MCP server.

    Args:
        mcp: FastMCP server instance
        trading: Trading instance
        enabled_tools: List of enabled tool names
    """

    if "create_order" in enabled_tools:

        @mcp.tool()
        def create_order(
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
                quantity: Order quantity (required for most order types)
                quote_order_qty: Quote order quantity (for MARKET BUY orders)
                price: Order price (required for LIMIT orders)
                time_in_force: Time in force - 'GTC', 'IOC', 'FOK' (required for LIMIT orders)
                stop_price: Stop price (required for STOP orders)
                iceberg_qty: Iceberg quantity for iceberg orders
                new_client_order_id: Custom order ID

            Returns:
                dict: Order creation response with order details
            """
            return trading.create_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                quote_order_qty=quote_order_qty,
                price=price,
                time_in_force=time_in_force,
                stop_price=stop_price,
                iceberg_qty=iceberg_qty,
                new_client_order_id=new_client_order_id,
            )

    if "test_order" in enabled_tools:

        @mcp.tool()
        def test_order(
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
                quote_order_qty: Quote order quantity (for MARKET BUY orders)
                price: Order price (required for LIMIT orders)
                time_in_force: Time in force - 'GTC', 'IOC', 'FOK'

            Returns:
                dict: Empty dict if validation passes, otherwise error
            """
            return trading.test_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                quote_order_qty=quote_order_qty,
                price=price,
                time_in_force=time_in_force,
            )

    if "cancel_order" in enabled_tools:

        @mcp.tool()
        def cancel_order(
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
            """
            return trading.cancel_order(
                symbol=symbol, order_id=order_id, orig_client_order_id=orig_client_order_id
            )

    if "get_order" in enabled_tools:

        @mcp.tool()
        def get_order(
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
                dict: Order information including status and filled amount
            """
            return trading.get_order(
                symbol=symbol, order_id=order_id, orig_client_order_id=orig_client_order_id
            )

    logger.info(f"Registered {len(enabled_tools)} trading tools")
