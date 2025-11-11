"""Configuration file loader."""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Load and manage configuration from YAML file."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize ConfigLoader.

        Args:
            config_path: Path to config.yaml file. If None, uses default location.
        """
        if config_path:
            self.config_path = Path(config_path)
        else:
            # Default to config.yaml in project root
            self.config_path = Path(__file__).parent.parent.parent / "config.yaml"

        self.config: Dict[str, Any] = {}

    def load(self) -> Dict[str, Any]:
        """Load configuration from YAML file.

        Returns:
            dict: Loaded configuration

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is invalid
        """
        if not self.config_path.exists():
            logger.error(f"Config file not found: {self.config_path}")
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f) or {}
            logger.info(f"Configuration loaded from {self.config_path}")
            return self.config
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in config file: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to load config file: {e}")
            raise

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: Configuration key (supports dot notation, e.g., 'tools.market.enabled')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def is_tool_enabled(self, category: str, tool_name: str) -> bool:
        """Check if a specific tool is enabled.

        Args:
            category: Tool category (e.g., 'market', 'trading')
            tool_name: Tool name (e.g., 'get_symbol_ticker')

        Returns:
            bool: True if tool is enabled, False otherwise
        """
        # Check if category is enabled
        category_enabled = self.get(f"tools.{category}.enabled", False)
        if not category_enabled:
            return False

        # Check if tool is in the enabled tools list
        enabled_tools = self.get(f"tools.{category}.tools", [])
        return tool_name in enabled_tools

    def get_enabled_tools(self, category: str) -> list:
        """Get list of enabled tools for a category.

        Args:
            category: Tool category (e.g., 'market', 'trading')

        Returns:
            list: List of enabled tool names
        """
        category_enabled = self.get(f"tools.{category}.enabled", False)
        if not category_enabled:
            return []

        return self.get(f"tools.{category}.tools", [])

    def get_all_enabled_tools(self) -> Dict[str, list]:
        """Get all enabled tools grouped by category.

        Returns:
            dict: Dictionary with category as key and list of tool names as value
        """
        tools_config = self.get("tools", {})
        enabled_tools = {}

        for category, config in tools_config.items():
            if config.get("enabled", False):
                enabled_tools[category] = config.get("tools", [])

        return enabled_tools


def load_config(config_path: Optional[str] = None) -> ConfigLoader:
    """Load configuration file.

    Args:
        config_path: Path to config.yaml file. If None, uses default location.

    Returns:
        ConfigLoader: Loaded configuration loader instance
    """
    loader = ConfigLoader(config_path)
    loader.load()
    return loader
