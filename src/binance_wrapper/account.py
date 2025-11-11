"""Account related API wrapper."""

import logging
from typing import Optional
from .client import BinanceClient

logger = logging.getLogger(__name__)


class Account:
    """Wrapper for Binance Spot account APIs."""

    def __init__(self, binance_client: BinanceClient):
        """Initialize Account wrapper.

        Args:
            binance_client: BinanceClient instance
        """
        self.client = binance_client.get_client()

    def get_account_info(self) -> dict:
        """Get account information including balances.

        Returns:
            dict: Account information with balances and permissions

        Raises:
            Exception: If API request fails
        """
        try:
            result = self.client.account()
            logger.debug("Retrieved account information")
            return result
        except Exception as e:
            logger.error(f"Failed to get account info: {e}")
            raise

    def get_balance(self, asset: Optional[str] = None) -> dict:
        """Get account balance.

        Args:
            asset: Asset symbol (e.g., 'BTC', 'USDT'). If None, returns all balances.

        Returns:
            dict: Balance information for specified asset or all assets

        Raises:
            Exception: If API request fails
        """
        try:
            account_info = self.client.account()
            balances = account_info.get("balances", [])

            if asset:
                # Filter for specific asset
                for balance in balances:
                    if balance.get("asset") == asset:
                        logger.debug(f"Retrieved balance for {asset}: {balance}")
                        return balance
                # Asset not found
                logger.warning(f"Asset {asset} not found in balances")
                return {"asset": asset, "free": "0.00000000", "locked": "0.00000000"}
            else:
                # Return all non-zero balances
                non_zero_balances = [
                    b
                    for b in balances
                    if float(b.get("free", 0)) > 0 or float(b.get("locked", 0)) > 0
                ]
                logger.debug(f"Retrieved {len(non_zero_balances)} non-zero balances")
                return {"balances": non_zero_balances}
        except Exception as e:
            logger.error(f"Failed to get balance: {e}")
            raise

    def get_account_status(self) -> dict:
        """Get account API trading status.

        Returns:
            dict: Account API trading status

        Raises:
            Exception: If API request fails
        """
        try:
            result = self.client.account_status()
            logger.debug("Retrieved account status")
            return result
        except Exception as e:
            logger.error(f"Failed to get account status: {e}")
            raise

    def get_account_api_permissions(self) -> dict:
        """Get account API key permissions.

        Returns:
            dict: API key permissions

        Raises:
            Exception: If API request fails
        """
        try:
            result = self.client.account_api_permissions()
            logger.debug("Retrieved API permissions")
            return result
        except Exception as e:
            logger.error(f"Failed to get API permissions: {e}")
            raise
