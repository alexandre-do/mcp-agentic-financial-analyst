import os

import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")


def _call_alpha_vantage(params: dict) -> dict | str:
    """Call the Alpha Vantage REST API and return the parsed JSON payload.

    Returns an error string instead of raising so tool calls can surface the
    failure to the agent as a normal tool result.
    """
    if not ALPHA_VANTAGE_API_KEY:
        return "Error: ALPHA_VANTAGE_API_KEY is not set in the environment."

    response = requests.get(
        ALPHA_VANTAGE_BASE_URL,
        params={**params, "apikey": ALPHA_VANTAGE_API_KEY},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    # Alpha Vantage returns HTTP 200 even for errors/rate limits, so these
    # keys have to be checked explicitly.
    if "Error Message" in data:
        return f"Error: {data['Error Message']}"
    if "Note" in data:
        return f"Error: {data['Note']}"
    if "Information" in data:
        return f"Error: {data['Information']}"

    return data


@tool
def get_stock_quote(symbol: str) -> str:
    """Get the latest quote (price, volume, change) for a stock ticker symbol.

    Args:
        symbol: The stock ticker symbol, e.g. "AAPL" or "MSFT".
    """
    result = _call_alpha_vantage({"function": "GLOBAL_QUOTE", "symbol": symbol})
    if isinstance(result, str):
        return result
    return str(result.get("Global Quote", result))


@tool
def get_daily_time_series(symbol: str, outputsize: str = "compact") -> str:
    """Get daily OHLCV time series data for a stock ticker symbol.

    Args:
        symbol: The stock ticker symbol, e.g. "AAPL" or "MSFT".
        outputsize: "compact" for the latest 100 data points, or "full" for
            the full 20+ years of history.
    """
    result = _call_alpha_vantage(
        {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": outputsize,
        }
    )
    if isinstance(result, str):
        return result
    return str(result.get("Time Series (Daily)", result))


@tool
def get_company_overview(symbol: str) -> str:
    """Get company fundamentals (sector, market cap, P/E ratio, EPS, etc.) for a stock ticker symbol.

    Args:
        symbol: The stock ticker symbol, e.g. "AAPL" or "MSFT".
    """
    result = _call_alpha_vantage({"function": "OVERVIEW", "symbol": symbol})
    if isinstance(result, str):
        return result
    return str(result)


@tool
def search_symbol(keywords: str) -> str:
    """Search for stock ticker symbols matching a company name or keyword.

    Args:
        keywords: Free-text search terms, e.g. "Apple" or "microsoft".
    """
    result = _call_alpha_vantage({"function": "SYMBOL_SEARCH", "keywords": keywords})
    if isinstance(result, str):
        return result
    return str(result.get("bestMatches", result))
