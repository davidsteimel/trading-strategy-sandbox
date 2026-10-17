from alpaca.data.requests import StockBarsRequest
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame

from datetime import datetime
from pathlib import Path
import plotly.graph_objects as go
import pandas as pd
import hashlib
import math
import os

from dotenv import load_dotenv

ROOT      = Path(__file__).parent.parent
DATA_DIR  = ROOT / "data"
CACHE_DIR = DATA_DIR / "cache"

def _cache_path(
    symbols: list[str], start_date: datetime, end_date: datetime, adjustment: str
) -> Path:
  """Create a cache path for the given symbols and date range."""

  symbol_hash = hashlib.md5("_".join(sorted(symbols)).encode()).hexdigest()[:10]
  start_str = start_date.strftime("%Y-%m-%d")
  end_str = end_date.strftime("%Y-%m-%d")

  return CACHE_DIR / f"{symbol_hash}_{start_str}_{end_str}_{adjustment}.parquet"

def get_stock_data(
        symbols: list[str] | str,
        start_date: datetime,
        end_date: datetime,
        adjustment: str = "all"
):
    """
    Get stock data for the given symbols and date range.
    Returns a DataFrame with the stock data, either from cache or from the Alpaca API.
    """

    if isinstance(symbols, str):
        symbols = [symbols]

    cache_file = _cache_path(symbols, start_date, end_date, adjustment)

    # check if cache file exists and load from it if it does
    if cache_file.exists():
        print(f"[DataLoader] Cache hit: {cache_file.name}")
        return pd.read_parquet(cache_file)
    
    load_dotenv()
    stock_client = StockHistoricalDataClient(
        api_key=os.getenv("ALPACA_API_KEY"),
        secret_key=os.getenv("ALPACA_SECRET_KEY")
    )
    bars_request_params = StockBarsRequest(
    symbol_or_symbols=symbols,
    timeframe=TimeFrame.Day,
    start=start_date,
    end=end_date,
    adjustment=adjustment
)
    print(f"[DataLoader] Cache miss. Downloading from Alpaca API...")
    df = stock_client.get_stock_bars(bars_request_params).df

    if df.empty:
        raise ValueError("API returned no data for the given parameters.")

    df = df.sort_index(level=['symbol', 'timestamp'])

    returned_symbols = df.index.get_level_values('symbol').unique()
    missing_symbols = [s for s in symbols if s not in returned_symbols]
    if missing_symbols:
        print(f"[DataLoader] Warning: No data found for the following symbols: {missing_symbols}")

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(cache_file)

    return df