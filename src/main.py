import backtrader as bt
from datetime import datetime
from src.dataloader import get_feed

# 1. (Hier würdest du später z.B. import src.strategies.sma_crossover import SMACross machen)
# Für den Moment nehmen wir eine leere Test-Strategie
class TestStrategy(bt.Strategy):
    def next(self):
        # Das wird jeden Tag aufgerufen. Hier kommt später die Logik rein!
        pass 

if __name__ == '__main__':
    # 2. Das Gehirn (Engine) initialisieren
    cerebro = bt.Cerebro()

    # 3. Startkapital setzen (z.B. 10.000$)
    cerebro.broker.setcash(10000.0)

    # 4. Daten holen (über unseren neuen Feed-Adapter!)
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 31)
    
    apple_feed = get_feed("AAPL", start=start_date, end=end_date)
    
    # 5. Daten und Strategie an Cerebro übergeben
    cerebro.adddata(apple_feed)
    cerebro.addstrategy(TestStrategy)

    print(f'Startkapital: {cerebro.broker.getvalue():.2f}')
    
    # 6. Backtest starten
    cerebro.run()
    
    print(f'Endkapital: {cerebro.broker.getvalue():.2f}')
    
    # 7. Ergebnisse zeichnen (Das ist dein "Visualize")
    # cerebro.plot(style='candlestick') # <- Einfach einkommentieren für den Chart