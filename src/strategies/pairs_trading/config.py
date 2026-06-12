from dataclasses import dataclass, field
from datetime import datetime

from src.config import (
    DEFAULT_START, DEFAULT_END, OOS_START, OOS_END,
    SP400, WATCHLIST, SECTOR_MAP, MIN_HISTORY_DAYS, PRICE_COLUMN
)

@dataclass(frozen=True)
class PairsConfig:
    """
    Immutable Konfiguration für einen Pairs-Trading-Backtest.
    frozen=True: Parameter können nach Instanziierung nicht verändert werden
                 → verhindert versehentliche Mutation während Backtest-Runs.
    """

    # Welche Symbol-Liste für das Screening verwendet wird.
    # Empfehlung: Für Entwicklung WATCHLIST, für Produktion SP400.
    universe: list[str] = field(default_factory=lambda: WATCHLIST)

    # Nur Paare innerhalb desselben Sektors testen?
    # Erhöht ökonomische Plausibilität, reduziert Paare drastisch.
    sector_neutral: bool = True

    # ── Zeitrahmen ───────────────────────────────────────────────────────────
    start:     datetime = DEFAULT_START
    end:       datetime = DEFAULT_END
    oos_start: datetime = OOS_START
    oos_end:   datetime = OOS_END

    # ── Kointegrations-Screening ─────────────────────────────────────────────
    # Engle-Granger p-Wert Schwelle (vor FDR-Korrektur)
    coint_pvalue_raw: float = 0.05

    # FDR-Korrektur-Methode: "fdr_bh" (Benjamini-Hochberg) empfohlen
    # Alternativen: "bonferroni", "fdr_by", None (kein Correction)
    fdr_method: str = "fdr_bh"

    # FDR-adjustierter Alpha-Level
    coint_pvalue_fdr: float = 0.05

    # Mindestanzahl gemeinsamer Handelstage für ein valides Paar
    min_common_days: int = MIN_HISTORY_DAYS   # = 252

    # ── Spread / OU-Prozess ──────────────────────────────────────────────────
    # Methode zur Hedge-Ratio-Schätzung:
    #   "ols"    – statische OLS-Regression (einfach, schnell)
    #   "kalman" – dynamische Kalman-Filter-Schätzung (robuster, komplexer)
    hedge_method: str = "kalman"

    # Lookback-Fenster für rollende Kalman-/OLS-Schätzung (in Tagen)
    hedge_lookback: int = 60

    # ── Einstiegs- / Ausstiegs-Schwellen (z-Score des Spreads) ───────────────
    # Klassische Parametrisierung: Entry bei ±2σ, Exit bei 0, Stop bei ±3σ
    z_entry:  float = 2.0   # |z| > z_entry  → Position öffnen
    z_exit:   float = 0.0   # |z| < z_exit   → Position schließen
    z_stop:   float = 3.0   # |z| > z_stop   → Hard Stop-Loss

    # Lookback für z-Score Normalisierung (rollende Std / Mean)
    z_lookback: int = 20

    # ── Halbwertszeit-Filter ─────────────────────────────────────────────────
    # Nur Paare handeln deren OU-Halbwertszeit im sinnvollen Bereich liegt.
    # Zu kurz → Transaktionskosten fressen Alpha; zu lang → kein mean-reversion.
    halflife_min: int = 5    # Handelstage
    halflife_max: int = 60   # Handelstage

    # ── Positionsgröße & Risiko ──────────────────────────────────────────────
    # Anteil des Gesamtkapitals pro Paar (beidseitig, long + short)
    capital_per_pair: float = 0.10   # 10 % pro Paar → max 10 simultane Paare

    # Maximale Anzahl simultaner offener Paare
    max_open_pairs: int = 10

    # Stop-Loss auf Paar-Ebene (relativer Verlust, beidseitig gemessen)
    pair_stop_loss: float = 0.05   # 5 % Verlust → Position schließen

    # ── Transaktionskosten ───────────────────────────────────────────────────
    commission: float = 0.001   # 0.1 % pro Trade (realistisch für US-Aktien)
    slippage:   float = 0.001   # 0.1 % Slippage-Annahme

    # ── Daten-Parameter ─────────────────────────────────────────────────────
    price_col: str = PRICE_COLUMN   # = "close"


# ── Default-Instanz für direkten Import ─────────────────────────────────────
# Verwendung: from strategies.pairs_trading.config import PAIRS_CFG
PAIRS_CFG = PairsConfig()

# Produktions-Instanz mit vollem S&P 400 Universum
PAIRS_CFG_FULL = PairsConfig(universe=SP400, sector_neutral=True)