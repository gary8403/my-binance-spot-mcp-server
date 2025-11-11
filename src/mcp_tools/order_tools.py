"""MCP tools for order management."""

import logging
from typing import Optional
from ..binance_wrapper.order import OrderManagement

logger = logging.getLogger(__name__)


def register_order_tools(mcp, order_mgmt: OrderManagement, enabled_tools: list):
    """Register order management tools with MCP server.

    Args:
        mcp: FastMCP server instance
        order_mgmt: OrderManagement instance
        enabled_tools: List of enabled tool names
    """

    if "get_open_orders" in enabled_tools:

        @mcp.tool()
        def get_open_orders(symbol: Optional[str] = None) -> list:
            """Get all open orders.

            Args:
                symbol: Trading pair symbol (e.g., 'BTCUSDT'). If not provided, returns all symbols.

            Returns:
                list: List of open orders
            """
            return order_mgmt.get_open_orders(symbol)

    if "get_all_orders" in enabled_tools:

        @mcp.tool()
        def get_all_orders(
            symbol: str,
            order_id: Optional[int] = None,
            start_time: Optional[int] = None,
            end_time: Optional[int] = None,
            limit: int = 500,
        ) -> list:
            """Get all orders (active, canceled, filled).

            Args:
                symbol: Trading pair symbol (e.g., 'BTCUSDT')
                order_id: Order ID to fetch orders from (optional)
                start_time: Start time in milliseconds (optional)
                end_time: End time in milliseconds (optional)
                limit: Number of orders (default: 500, max: 1000)

            Returns:
                list: List of all orders
            """
            return order_mgmt.get_all_orders(symbol, order_id, start_time, end_time, limit)

    if "cancel_all_orders" in enabled_tools:

        @mcp.tool()
        def cancel_all_orders(symbol: str) -> list:
            """Cancel all open orders on a symbol.

            Args:
                symbol: Trading pair symbol (e.g., 'BTCUSDT')

            Returns:
                list: List of cancelled orders
            """
            return order_mgmt.cancel_all_orders(symbol)

    if "cancel_open_orders" in enabled_tools:

        @mcp.tool()
        def cancel_open_orders(symbol: str) -> list:
            """Cancel all open orders on a symbol (alias for cancel_all_orders).

            Args:
                symbol: Trading pair symbol (e.g., 'BTCUSDT')

            Returns:
                list: List of cancelled orders
            """
            return order_mgmt.cancel_open_orders(symbol)

    logger.info(f"Registered {len(enabled_tools)} order management tools")
