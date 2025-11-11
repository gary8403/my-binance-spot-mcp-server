"""Configuration validator."""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class ConfigValidator:
    """Validate configuration structure and values."""

    # Valid tool categories
    VALID_CATEGORIES = ["market", "trading", "account", "order"]

    # Valid tools for each category
    VALID_TOOLS = {
        "market": [
            "get_symbol_ticker",
            "get_orderbook",
            "get_klines",
            "get_trades",
            "get_24hr_ticker",
            "get_avg_price",
            "get_exchange_info",
        ],
        "trading": [
            "create_order",
            "test_order",
            "cancel_order",
            "get_order",
        ],
        "account": [
            "get_account_info",
            "get_balance",
            "get_account_status",
        ],
        "order": [
            "get_open_orders",
            "get_all_orders",
            "cancel_all_orders",
            "cancel_open_orders",
        ],
    }

    def __init__(self, config: Dict[str, Any]):
        """Initialize ConfigValidator.

        Args:
            config: Configuration dictionary to validate
        """
        self.config = config
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> bool:
        """Validate the configuration.

        Returns:
            bool: True if valid, False otherwise
        """
        self.errors = []
        self.warnings = []

        # Check if 'tools' key exists
        if "tools" not in self.config:
            self.errors.append("Missing 'tools' key in configuration")
            return False

        tools_config = self.config["tools"]

        # Validate each category
        for category in tools_config:
            if category not in self.VALID_CATEGORIES:
                self.warnings.append(f"Unknown tool category: {category}")
                continue

            self._validate_category(category, tools_config[category])

        # Log validation results
        if self.errors:
            for error in self.errors:
                logger.error(f"Config validation error: {error}")
            return False

        if self.warnings:
            for warning in self.warnings:
                logger.warning(f"Config validation warning: {warning}")

        logger.info("Configuration validation successful")
        return True

    def _validate_category(self, category: str, config: Dict[str, Any]) -> None:
        """Validate a tool category configuration.

        Args:
            category: Category name
            config: Category configuration
        """
        # Check if 'enabled' key exists
        if "enabled" not in config:
            self.errors.append(f"Missing 'enabled' key for category '{category}'")
            return

        # Check if 'enabled' is boolean
        if not isinstance(config["enabled"], bool):
            self.errors.append(f"'enabled' must be boolean for category '{category}'")
            return

        # If category is disabled, skip tool validation
        if not config["enabled"]:
            return

        # Check if 'tools' key exists
        if "tools" not in config:
            self.errors.append(f"Missing 'tools' key for category '{category}'")
            return

        # Check if 'tools' is a list
        if not isinstance(config["tools"], list):
            self.errors.append(f"'tools' must be a list for category '{category}'")
            return

        # Validate each tool in the list
        valid_tools = self.VALID_TOOLS.get(category, [])
        for tool in config["tools"]:
            if tool not in valid_tools:
                self.warnings.append(
                    f"Unknown tool '{tool}' in category '{category}'. "
                    f"Valid tools: {', '.join(valid_tools)}"
                )

    def get_errors(self) -> List[str]:
        """Get validation errors.

        Returns:
            list: List of error messages
        """
        return self.errors

    def get_warnings(self) -> List[str]:
        """Get validation warnings.

        Returns:
            list: List of warning messages
        """
        return self.warnings


def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration.

    Args:
        config: Configuration dictionary

    Returns:
        bool: True if valid, False otherwise
    """
    validator = ConfigValidator(config)
    return validator.validate()
