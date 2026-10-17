import pandas as pd
import math




def run_backtest(start_capital, stocks, df, target_positions, weights=None):
    """"Long-or-Cash-Simulation. 
    Only separate initial capitals, execution at the next open,
    fractional shares allowed, no costs and no short positions. 
    """
    execution_target = target_positions.loc[:, stocks].sort_index().shift(1)
    if weights is None:
        weights = {stock: (1 / len(stocks)) for stock in stocks}

    portfolio = {
      "stocks": {
          stock: {
              "cash": float(start_capital * weights[stock]),
              "shares": 0.0,
          }
          for stock in stocks
      },
      "depo_value": float(start_capital),
    }
    daily_portfolio_value = pd.Series(index=execution_target.index, dtype=float)

    for timestamp, row in execution_target.iterrows():
        for stock in portfolio["stocks"]:
            target_today = row[stock]
            holding = portfolio["stocks"][stock]

            if pd.isna(target_today):
                continue

            if target_today == 1 and holding["shares"] == 0:
                price = float(df.loc[(stock, timestamp), "open"])
                holding["shares"] = (holding["cash"]) / price
                holding["cash"] = 0.0

            elif target_today == 0 and holding["shares"] > 0:
                price = float(df.loc[(stock, timestamp), "open"])
                holding["cash"] += holding["shares"] * price
                holding["shares"] = 0.0
            
            daily_portfolio_value.loc[timestamp] = sum(
                holding["cash"] + holding["shares"] * df.loc[(stock, timestamp), "close"]
                for stock, holding in portfolio["stocks"].items()
            )

    portfolio["depo_value"] = round(float(sum(
        holding["cash"] + holding["shares"] * df.loc[(stock, execution_target.index[-1]), "close"]
        for stock, holding in portfolio["stocks"].items())), 2)

    return portfolio, daily_portfolio_value