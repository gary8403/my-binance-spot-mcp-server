# Binance Spot MCP Server

A Model Context Protocol (MCP) server that wraps the Binance Spot API, enabling AI models to interact with Binance Spot trading exchange through standardized MCP tools.

## Overview

This project packages the Binance Spot official SDK as an MCP server using the FastMCP framework. It provides a secure, configurable interface for AI models to perform trading operations, query market data, manage accounts, and handle orders on Binance Spot.

## Features

- **Complete Binance Spot API Coverage**: All major Binance Spot endpoints wrapped as MCP tools
- **Secure Authentication**: API key and secret management via environment variables
- **Token Verification**: MCP token-based authentication for secure access
- **Flexible Configuration**: YAML-based tool configuration to selectively enable/disable features
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Modular Architecture**: Clean separation of concerns for easy maintenance and extension

## Architecture

```
         AI Model / MCP Client           
                  | MCP Protocol
                  |
         FastMCP Server                   
   |-- Token Verification              
   |-- MCP Tool Handlers               
                  |
      Binance SDK Wrapper Layer          
   |-- Market Data Tools              
   |-- Trading Tools                  
   |-- Account Tools                  
   |-- Order Management Tools           
                  |
      Binance Spot API                   
```

## Installation

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip for package management
- Binance API key and secret

### Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone <repository-url>
cd my-binance-spot-mcp-server

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Note: PySocks is included for SOCKS5 proxy support
```

### Using pip

```bash
# Clone the repository
git clone <repository-url>
cd my-binance-spot-mcp-server

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Note: PySocks is included for SOCKS5 proxy support
```

## Configuration

### 1. Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Binance API Credentials
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here

# MCP Server Token (used for FastMCP Token Verification)
TOKEN=your_mcp_server_token_here

# Optional: Binance API Base URL (default: https://api.binance.com)
# BINANCE_BASE_URL=https://api.binance.com

# Optional: Enable testnet mode (default: false)
# BINANCE_TESTNET=false

# Optional: Proxy Configuration
# Supported proxy types: http, https, socks5
# HTTP/HTTPS Proxy example: http://proxy.example.com:8080
# SOCKS5 Proxy example: socks5://proxy.example.com:1080
# With authentication: http://username:password@proxy.example.com:8080
# PROXY_URL=
```

**⚠️ Security Warning**: Never commit the `.env` file to version control!

#### Proxy Configuration

The server supports HTTP, HTTPS, and SOCKS5 proxies for connecting to Binance API:

1. **HTTP/HTTPS Proxy**:
   ```env
   PROXY_URL=http://proxy.example.com:8080
   ```

2. **SOCKS5 Proxy**:
   ```env
   PROXY_URL=socks5://proxy.example.com:1080
   ```

   Note: SOCKS5 support requires the `PySocks` library (included in requirements.txt)

3. **Proxy with Authentication**:
   ```env
   PROXY_URL=http://username:password@proxy.example.com:8080
   ```

4. **No Proxy** (default):
   Simply leave `PROXY_URL` unset or commented out in your `.env` file

**Use Cases**:
- Accessing Binance API from restricted networks
- Routing traffic through specific geographic locations
- Corporate network environments requiring proxy usage
- Enhanced privacy and security

### 2. Tool Configuration

Edit `config.yaml` to enable/disable specific tools:

```yaml
tools:
  # Market Data Tools
  market:
    enabled: true
    tools:
      - get_symbol_ticker
      - get_orderbook
      - get_klines
      - get_trades
      - get_24hr_ticker
      - get_avg_price
      - get_exchange_info

  # Trading Tools
  trading:
    enabled: true
    tools:
      - create_order
      - test_order
      - cancel_order
      - get_order

  # Account Tools
  account:
    enabled: true
    tools:
      - get_account_info
      - get_balance
      - get_account_status

  # Order Management Tools
  order:
    enabled: true
    tools:
      - get_open_orders
      - get_all_orders
      - cancel_all_orders
      - cancel_open_orders
```

## Usage

### Starting the Server

```bash
# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run the server
python main.py
```

The server will start and listen for MCP protocol connections.

### Token Verification

The server implements automatic token verification for secure access:

1. **How it works**:
   - When the server starts, it automatically enables token verification if the FastMCP auth module is available
   - All MCP requests must include the token in the `Authorization` header
   - Format: `Authorization: Bearer <your_token_from_env>`

2. **Checking verification status**:
   - On startup, check the logs for "Token verification enabled" message
   - If you see "WARNING: Server is running in insecure mode!", token verification failed to initialize

3. **Client configuration**:
   - Ensure your MCP client sends the Authorization header with each request
   - The token must match the `TOKEN` value in your `.env` file

4. **Troubleshooting token verification**:
   - If token verification is unavailable, check FastMCP installation
   - The server will still run but without authentication (logged as warning)
   - Consider updating FastMCP to the latest version if auth is not available

### Available Tools

#### Market Data Tools

- **get_symbol_ticker**: Get current price for a trading pair
- **get_orderbook**: Get order book depth
- **get_klines**: Get candlestick/kline data
- **get_trades**: Get recent trades
- **get_24hr_ticker**: Get 24hr price change statistics
- **get_avg_price**: Get average price
- **get_exchange_info**: Get exchange trading rules and symbol information

#### Trading Tools

- **create_order**: Create a new order (MARKET, LIMIT, STOP, etc.)
- **test_order**: Test order creation without actually placing it
- **cancel_order**: Cancel an active order
- **get_order**: Check an order's status

#### Account Tools

- **get_account_info**: Get account information including all balances
- **get_balance**: Get balance for specific asset or all non-zero balances
- **get_account_status**: Get account API trading status

#### Order Management Tools

- **get_open_orders**: Get all open orders
- **get_all_orders**: Get all orders (active, canceled, filled)
- **cancel_all_orders**: Cancel all open orders on a symbol
- **cancel_open_orders**: Cancel all open orders (alias)

## Project Structure

```
my-binance-spot-mcp-server/
├── main.py                    # Main entry point
├── .env                       # Environment variables (not in git)
├── .env.example               # Environment variables template
├── config.yaml                # MCP tool configuration
├── requirements.txt           # Python dependencies
├── pyproject.toml             # Project configuration
├── README.md                  # This file
├── LICENSE                    # License file
├── binance_mcp_server.log     # Server logs (generated)
└── src/                       # Source code
    ├── __init__.py
    ├── binance_wrapper/       # Binance SDK wrapper layer
    │   ├── __init__.py
    │   ├── client.py          # Binance client initialization
    │   ├── market.py          # Market data API wrapper
    │   ├── trading.py         # Trading API wrapper
    │   ├── account.py         # Account API wrapper
    │   └── order.py           # Order management API wrapper
    ├── mcp_tools/             # MCP tool definitions
    │   ├── __init__.py
    │   ├── market_tools.py    # Market data tools
    │   ├── trading_tools.py   # Trading tools
    │   ├── account_tools.py   # Account tools
    │   └── order_tools.py     # Order management tools
    └── config/                # Configuration management
        ├── __init__.py
        ├── loader.py          # Configuration loader
        └── validator.py       # Configuration validator
```

## Development

### Adding New Tools

1. **Add wrapper method**: Implement the API call in the appropriate wrapper file in `src/binance_wrapper/`
2. **Define MCP tool**: Create the MCP tool in the corresponding file in `src/mcp_tools/`
3. **Update configuration**: Add the tool to `config.yaml`
4. **Update validator**: Add the tool name to valid tools list in `src/config/validator.py`

### Logging

Logs are written to both console and `binance_mcp_server.log` file. Log levels can be adjusted in `main.py`.

## Security Considerations

1. **API Keys**:
   - Never commit `.env` file to version control
   - Use API keys with minimal required permissions
   - Regularly rotate API keys
   - Consider using Binance testnet for development

2. **Token Verification**:
   - The server implements token-based authentication using FastMCP's auth system
   - Clients must include the token in request headers: `Authorization: Bearer <your_token>`
   - Use strong, randomly generated tokens (minimum 32 characters recommended)
   - Keep the TOKEN value secret and never commit it to version control
   - Rotate tokens periodically for enhanced security
   - The server will log warnings if token verification is unavailable (check logs on startup)

3. **Network Security**:
   - Use HTTPS for all API communications (default)
   - Consider IP whitelisting on Binance API keys
   - Monitor API usage for suspicious activity

4. **Rate Limits**:
   - Be aware of Binance API rate limits
   - Implement appropriate error handling for rate limit errors
   - Consider implementing request throttling

## Testing

### Using Testnet

Set `BINANCE_TESTNET=true` in your `.env` file to use Binance testnet:

```env
BINANCE_TESTNET=true
```

You'll need testnet API keys from [https://testnet.binance.vision/](https://testnet.binance.vision/)

## Troubleshooting

### Connection Issues

- Verify your API key and secret are correct
- Check if your IP is whitelisted (if IP restriction is enabled)
- Ensure you have internet connectivity
- Check Binance API status

### Proxy Issues

- **Connection timeout or failure**:
  - Verify the proxy URL format is correct (e.g., `http://host:port` or `socks5://host:port`)
  - Ensure the proxy server is accessible from your network
  - Test proxy connectivity using curl: `curl -x <PROXY_URL> https://api.binance.com/api/v3/ping`

- **SOCKS5 proxy not working**:
  - Ensure PySocks is installed: `pip install PySocks` or `uv pip install PySocks`
  - Check proxy authentication credentials if required

- **Proxy authentication errors**:
  - Verify username and password are correct in the proxy URL
  - Ensure special characters in credentials are URL-encoded
  - Format: `http://username:password@host:port`

- **Corporate proxy certificates**:
  - Some corporate proxies use custom SSL certificates
  - You may need to install the corporate certificate in your system's trust store

### Configuration Errors

- Validate your `config.yaml` syntax
- Check logs for validation errors
- Ensure all enabled tools are spelled correctly

### API Errors

- Check the log file for detailed error messages
- Verify you have the required permissions for the operation
- Check Binance API documentation for specific error codes

## References

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Binance Spot API Documentation](https://binance-docs.github.io/apidocs/spot/en/)
- [Binance Python SDK](https://github.com/binance/binance-connector-python)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## License

[MIT License]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This software is for educational and research purposes only. Use at your own risk. The authors are not responsible for any financial losses incurred through the use of this software. Always test thoroughly with small amounts or on testnet before using in production.
