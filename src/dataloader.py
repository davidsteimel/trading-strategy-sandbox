from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import backtrader as bt
from datetime import datetime
from pathlib import Path
import hashlib
import warnings
import os
from src import config

from alpaca.data.historical import StockHistoricalDataClient
from dotenv import load_dotenv
import pandas as pd

CACHE_DIR = config.CACHE_DIR
CACHE_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv()
stock_client = StockHistoricalDataClient(
    api_key=os.getenv("ALPACA_API_KEY"),
    secret_key=os.getenv("ALPACA_SECRET_KEY")
)

def _cache_path(symbols: list[str], start_str: str, end_str: str) -> Path:
    """Kollisionssicherer Cache-Key via MD5-Hash der sortierten Symbolliste."""
    symbol_hash = hashlib.md5("_".join(sorted(symbols)).encode()).hexdigest()[:10]
    return CACHE_DIR / f"{symbol_hash}_{start_str}_{end_str}.parquet"

def get_stock_data(
    symbols: list[str] | str,
    start: datetime,
    end: datetime,
    strict: bool = False  # True = alter Verhalten (raise bei missing)
) -> pd.DataFrame:
    """
    Loads historical stock data for the given symbols and date range.
    Processes data for backtrader and saves it to cache for future use.

    Args:
        symbols (list or str): "AAPL" or ["AAPL", "NVDA", "TSLA"]

        start (datetime): Startdate for the data (inclusive).

        end (datetime): Enddate for the data (inclusive).
                        For example: datetime(2020, 1, 1)

    Returns:
        pd.DataFrame: DataFrame with columns
                      ['symbol', 'open', 'high', 'low', 'close', 'volume'].
                      
    Raises:
        ValueError: If 'symbols' is neither a string nor a list.
    """

    # check if symbols is a string and convert to list if necessary
    if isinstance(symbols, str):
        symbols = [symbols]
    elif not isinstance(symbols, list):
        raise ValueError("Symbols must be a list or a string.")

    # format start and end date to string for cache filename
    start_str = start.strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")
    
    cache_file = _cache_path(symbols, start_str, end_str)

    # check if cache file exists and load from it if it does
    if cache_file.exists():
        print(f"[DataLoader] Cache hit: {cache_file.name}")
        return pd.read_parquet(cache_file)
    
    # else load from API
    print(f"[DataLoader] Fetching {len(symbols)} symbols from API...")
    request_params = StockBarsRequest(
        symbol_or_symbols=symbols,
        timeframe=TimeFrame.Day,
        start=start,
        end=end,
        adjustment="all"
    )
    
    bars = stock_client.get_stock_bars(request_params)
    df = bars.df.reset_index()

    # Symbol-Validierung
    returned = set(df['symbol'].unique())
    missing  = set(symbols) - returned
    if missing:
        msg = f"[DataLoader] {len(missing)}/{len(symbols)} symbols missing: {sorted(missing)}"
        if strict:
            raise ValueError(msg)
        warnings.warn(msg, stacklevel=2)

    # Preprocessing
    df['timestamp'] = df['timestamp'].dt.tz_localize(None)
    df = (df
          .rename(columns={'timestamp': 'datetime'})
          [['datetime', 'symbol', 'open', 'high', 'low', 'close', 'volume']]
          .set_index('datetime'))

    df.to_parquet(cache_file)
    print(f"[DataLoader] Saved → {cache_file.name}  ({len(returned)} symbols, {len(df):,} rows)")

    return df

def get_feed(symbol: str, start: datetime, end: datetime) -> bt.feeds.PandasData:
    # load data using the common data loader
    df_all = get_stock_data([symbol], start, end)
    
    # filter for the specific symbol (in case multiple symbols were loaded)
    df_symbol = df_all[df_all['symbol'] == symbol]
    
    # create a backtrader feed from the DataFrame
    return bt.feeds.PandasData(
        dataname=df_symbol,
        datetime=None,
        open="open", high="high", low="low", close="close", volume="volume",
        openinterest=-1
    )