"""Binance Spot MCP Server - Main Entry Point."""

import os
import sys
import logging
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from fastmcp import FastMCP

# Try to import token verification classes
# The import path may vary depending on FastMCP version
try:
    from fastmcp.server.auth import TokenVerifier
    from fastmcp.server.auth.models import AccessToken
    TOKEN_VERIFICATION_AVAILABLE = True
except ImportError:
    try:
        from mcp.server.auth import TokenVerifier
        from mcp.server.auth.models import AccessToken
        TOKEN_VERIFICATION_AVAILABLE = True
    except ImportError:
        TOKEN_VERIFICATION_AVAILABLE = False
        TokenVerifier = None
        AccessToken = None

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.binance_wrapper.client import BinanceClient
from src.binance_wrapper.market import MarketData
from src.binance_wrapper.trading import Trading
from src.binance_wrapper.account import Account
from src.binance_wrapper.order import OrderManagement
from src.config.loader import load_config
from src.config.validator import validate_config
from src.mcp_tools.market_tools import register_market_tools
from src.mcp_tools.trading_tools import register_trading_tools
from src.mcp_tools.account_tools import register_account_tools
from src.mcp_tools.order_tools import register_order_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("binance_mcp_server.log")],
)
logger = logging.getLogger(__name__)


# Token Verification Implementation
if TOKEN_VERIFICATION_AVAILABLE:

    class SimpleTokenVerifier(TokenVerifier):
        """Simple static Token verifier.

        This verifier compares the incoming token with an expected token value
        loaded from environment variables.
        """

        def __init__(self, expected_token: str):
            """Initialize token verifier.

            Args:
                expected_token: Expected token value (from .env file)
            """
            self.expected_token = expected_token
            logger.info("Token verification enabled")

        def verify_token(self, token: str) -> Optional[AccessToken]:
            """Verify the provided token.

            Args:
                token: Token from the request

            Returns:
                AccessToken object if verification succeeds, None otherwise
            """
            if token == self.expected_token:
                logger.debug("Token verification successful")
                # Return a simple AccessToken object
                return AccessToken(
                    sub="mcp_client",  # Subject (client identifier)
                    scopes=[],  # Permission scopes (if needed)
                )
            logger.warning("Token verification failed")
            return None

else:
    logger.warning(
        "Token verification is not available. "
        "FastMCP auth module not found. Server will run without token verification."
    )


def load_environment():
    """Load environment variables from .env file.

    Returns:
        dict: Environment variables

    Raises:
        ValueError: If required environment variables are missing
    """
    # Load .env file
    load_dotenv()

    # Get required environment variables
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    token = os.getenv("TOKEN")

    # Validate required variables
    if not api_key:
        raise ValueError("BINANCE_API_KEY not found in environment variables")
    if not api_secret:
        raise ValueError("BINANCE_API_SECRET not found in environment variables")
    if not token:
        raise ValueError("TOKEN not found in environment variables")

    # Get optional variables
    base_url = os.getenv("BINANCE_BASE_URL")
    testnet = os.getenv("BINANCE_TESTNET", "false").lower() == "true"
    proxy_url = os.getenv("PROXY_URL")

    return {
        "api_key": api_key,
        "api_secret": api_secret,
        "token": token,
        "base_url": base_url,
        "testnet": testnet,
        "proxy_url": proxy_url,
    }


def initialize_binance_client(env_vars: dict) -> BinanceClient:
    """Initialize Binance client.

    Args:
        env_vars: Environment variables

    Returns:
        BinanceClient: Initialized Binance client
    """
    binance_client = BinanceClient(
        api_key=env_vars["api_key"],
        api_secret=env_vars["api_secret"],
        base_url=env_vars.get("base_url"),
        testnet=env_vars.get("testnet", False),
        proxy_url=env_vars.get("proxy_url"),
    )

    # Test connection
    try:
        binance_client.ping()
        logger.info("Successfully connected to Binance API")
    except Exception as e:
        logger.error(f"Failed to connect to Binance API: {e}")
        raise

    return binance_client


def register_all_tools(mcp: FastMCP, binance_client: BinanceClient, config):
    """Register all MCP tools based on configuration.

    Args:
        mcp: FastMCP server instance
        binance_client: BinanceClient instance
        config: Configuration loader
    """
    # Get all enabled tools from config
    enabled_tools = config.get_all_enabled_tools()

    logger.info(f"Registering tools for categories: {list(enabled_tools.keys())}")

    # Initialize wrapper instances
    market_data = MarketData(binance_client)
    trading = Trading(binance_client)
    account = Account(binance_client)
    order_mgmt = OrderManagement(binance_client)

    # Register market tools
    if "market" in enabled_tools:
        register_market_tools(mcp, market_data, enabled_tools["market"])

    # Register trading tools
    if "trading" in enabled_tools:
        register_trading_tools(mcp, trading, enabled_tools["trading"])

    # Register account tools
    if "account" in enabled_tools:
        register_account_tools(mcp, account, enabled_tools["account"])

    # Register order management tools
    if "order" in enabled_tools:
        register_order_tools(mcp, order_mgmt, enabled_tools["order"])

    logger.info("All tools registered successfully")


def main():
    """Main entry point for Binance Spot MCP Server."""
    try:
        logger.info("Starting Binance Spot MCP Server...")

        # 1. Load environment variables
        logger.info("Loading environment variables...")
        env_vars = load_environment()
        logger.info("Environment variables loaded")

        # 2. Load and validate configuration
        logger.info("Loading configuration...")
        config = load_config()
        logger.info("Configuration loaded")

        # 3. Validate configuration
        logger.info("Validating configuration...")
        if not validate_config(config.config):
            raise ValueError("Configuration validation failed")
        logger.info("Configuration validated")

        # 4. Initialize Binance client
        logger.info("Initializing Binance client...")
        binance_client = initialize_binance_client(env_vars)
        logger.info("Binance client initialized")

        # 5. Create FastMCP server with token verification
        logger.info("Creating FastMCP server...")

        if TOKEN_VERIFICATION_AVAILABLE:
            # Create token verifier
            token_verifier = SimpleTokenVerifier(expected_token=env_vars["token"])

            # Create FastMCP server with token verification enabled
            mcp = FastMCP("Binance Spot MCP Server", auth=token_verifier)
            logger.info("FastMCP server created with token verification enabled")
        else:
            # Create FastMCP server without token verification
            mcp = FastMCP("Binance Spot MCP Server")
            logger.warning("FastMCP server created WITHOUT token verification")
            logger.warning("WARNING: Server is running in insecure mode!")

        # 6. Register tools
        logger.info("Registering MCP tools...")
        register_all_tools(mcp, binance_client, config)
        logger.info("MCP tools registered")

        # 7. Start server
        logger.info("Starting MCP server...")
        mcp.run()

    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Failed to start server: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
