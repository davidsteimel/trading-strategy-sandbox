from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import backtrader as bt
from datetime import datetime

from pathlib import Path
from datetime import datetime

from alpaca.data.historical import StockHistoricalDataClient
from dotenv import load_dotenv
import os
import pandas as pd

# __file__ is src/dataloader.py → .parent is src/ → .parent is Root
# for each user the root is different,
# so we use __file__ to get the current file path and then navigate to the root
ROOT = Path(__file__).parent.parent
CACHE_DIR = ROOT / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv()
stock_client = StockHistoricalDataClient(api_key=os.getenv("ALPACA_API_KEY"),secret_key=os.getenv("ALPACA_SECRET_KEY"))

def get_stock_data(symbols: list, start: datetime, end: datetime) -> pd.DataFrame:
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
    
    # create a unique cache filename based on symbols and date range
    cache_file = CACHE_DIR / f"{'_'.join(sorted(symbols))}_{start_str}_{end_str}.parquet"

    # check if cache file exists and load from it if it does
    if cache_file.exists():
        print(f"Loading from cache: {cache_file.name}")
        return pd.read_parquet(cache_file)
    
    # else load from API
    print(f"Loading from API: {symbols}...")
    request_params = StockBarsRequest(
        symbol_or_symbols=symbols,
        timeframe=TimeFrame.Day,
        start=start,
        end=end,
        adjustment="all"  # adjusted data (dividends and splits)
    )
    
    bars = stock_client.get_stock_bars(request_params)
    df = bars.df

    # preprocess the data
    df = df.reset_index()
    df['timestamp'] = df['timestamp'].dt.tz_localize(None)
    df = df.rename(columns={'timestamp': 'datetime'})
    df = df[['datetime', 'symbol', 'open', 'high', 'low', 'close', 'volume']]
    df = df.set_index('datetime')
    
    # save to cache
    df.to_parquet(cache_file)
    print(f"[DataLoader] Saved to cache: {cache_file.name}")

    return df

def get_feed(symbol: str, start, end) -> bt.feeds.PandasData:
    # load data using the common data loader
    df_all = get_stock_data([symbol], start, end)
    
    # filter for the specific symbol (in case multiple symbols were loaded)
    df_symbol = df_all[df_all['symbol'] == symbol]
    
    # create a backtrader feed from the DataFrame
    feed = bt.feeds.PandasData(
        dataname=df_symbol,
        datetime=None, 
        open="open", high="high", low="low", close="close", volume="volume",
        openinterest=-1 # no open interest column, so we set it to -1 (ignored by backtrader)
    )
    return feed