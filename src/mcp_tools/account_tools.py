"""MCP tools for account management."""

import logging
from typing import Optional
from ..binance_wrapper.account import Account

logger = logging.getLogger(__name__)


def register_account_tools(mcp, account: Account, enabled_tools: list):
    """Register account tools with MCP server.

    Args:
        mcp: FastMCP server instance
        account: Account instance
        enabled_tools: List of enabled tool names
    """

    if "get_account_info" in enabled_tools:

        @mcp.tool()
        def get_account_info() -> dict:
            """Get account information including balances.

            Returns:
                dict: Account information with balances, permissions, and other details
            """
            return account.get_account_info()

    if "get_balance" in enabled_tools:

        @mcp.tool()
        def get_balance(asset: Optional[str] = None) -> dict:
            """Get account balance.

            Args:
                asset: Asset symbol (e.g., 'BTC', 'USDT'). If not provided, returns all non-zero balances.

            Returns:
                dict: Balance information for specified asset or all assets with non-zero balance
            """
            return account.get_balance(asset)

    if "get_account_status" in enabled_tools:

        @mcp.tool()
        def get_account_status() -> dict:
            """Get account API trading status.

            Returns:
                dict: Account API trading status including any restrictions
            """
            return account.get_account_status()

    logger.info(f"Registered {len(enabled_tools)} account tools")
