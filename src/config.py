"""
config.py  –  Configuration for Trading Strategy Sandbox
=========================================
Main config:
  - Paths
  - Dates / Timeframe Defaults
  - Universe Definitions (S&P 400 MidCap, Watchlist)
  - Data-Parameter
  - Logging

Stratgey specific config:
    - strategies/pairs_trading/config.py
"""

from pathlib import Path
from datetime import datetime

ROOT      = Path(__file__).parent.parent
DATA_DIR  = ROOT / "data"
CACHE_DIR = DATA_DIR / "cache"
LOG_DIR   = ROOT / "logs"
OUTPUT_DIR = ROOT / "output"

for _dir in (CACHE_DIR, LOG_DIR, OUTPUT_DIR):
    _dir.mkdir(parents=True, exist_ok=True)


# Backtesting Timeframe Defaults
DEFAULT_START: datetime = datetime(2018, 1, 1)
DEFAULT_END:   datetime = datetime(2023, 12, 31)

# Out-of-Sample Validation Timeframe
OOS_START: datetime = datetime(2024, 1, 1)
OOS_END:   datetime = datetime(2024, 12, 31)


TIMEFRAME         = "1Day"       # Alpaca TimeFrame-Mapping
PRICE_ADJUSTMENT  = "all"        # "all" = Dividenden + Splits abjusticated Data
MIN_HISTORY_DAYS  = 252          # Tradingdays per year
PRICE_COLUMN      = "close"      # standard price column for analysis



WATCHLIST: list[str] = [
    # Technology
    "NVDA", "AAPL", "MSFT", "AMD",
    # Financials
    "JPM", "GS", "BAC",
    # Energy
    "XOM", "CVX",
    # Consumer
    "AMZN", "COST",
    # Healthcare
    "JNJ", "PFE",
    # Industrials
    "CAT", "DE",
    # Utilities
    "NEE",
]


# ─────────────────────────────────────────────
# S&P 400 MIDCAP  –  vollständige Symbol-Liste
# ─────────────────────────────────────────────
# Quelle: S&P MidCap 400 Komponenten (Stand: 2024)
# Hinweis: Zusammensetzung ändert sich quartalsweise.
#          Für Survivorship-Bias-freie Analysen historische
#          Zusammensetzungen von einer Datenprovider-Quelle beziehen.

SP400: list[str] = [
    # A
    "AAN", "ABG", "ABM", "ACHC", "ACM", "ADMA", "AEO", "AFG", "AGCO",
    "AIT", "AJG", "AKAM", "ALB", "ALEX", "ALK", "ALLE", "AMKR", "AMN",
    "AMR", "APA", "ARI", "ARW", "ASB", "ASH", "ATI", "ATKR", "AVA",
    "AVNT", "AVT", "AWI",
    # B
    "BC", "BCO", "BDC", "BFH", "BGS", "BHE", "BJ", "BKH", "BLD",
    "BLKB", "BMI", "BNL", "BOH", "BOOT", "BRC", "BRX", "BSY", "BXMT",
    # C
    "CABO", "CALM", "CASY", "CBRE", "CBSH", "CBT", "CCSI", "CCS",
    "CEVA", "CFR", "CHE", "CHRD", "CLF", "CLIX", "CNM", "CNO", "COHU",
    "COLB", "COLL", "COLM", "COPT", "CPRI", "CPT", "CR", "CRAI",
    "CRI", "CRL", "CRS", "CSL", "CSWI", "CWT", "CXM",
    # D
    "DAR", "DBD", "DCI", "DCOM", "DDS", "DEI", "DEN", "DKS", "DLB",
    "DNOW", "DPZ", "DRH", "DV", "DVA",
    # E
    "EAT", "EGP", "ELF", "ENOV", "ENR", "ENS", "EPAY", "EPRT", "ESE",
    "ESNT", "ESRT", "EVR", "EXP",
    # F
    "FBNC", "FCF", "FCNCA", "FHI", "FHN", "FLO", "FLR", "FORM",
    "FPH", "FR", "FRME", "FUL", "FWRD",
    # G
    "GATX", "GEF", "GFF", "GHC", "GKOS", "GLNG", "GLOB", "GMED",
    "GNTY", "GPK", "GRBK", "GVA",
    # H
    "HAE", "HALO", "HAYW", "HBI", "HCSG", "HI", "HIW", "HLI", "HMST",
    "HNI", "HOG", "HOMB", "HP", "HPED", "HQY", "HR", "HTH", "HWC",
    # I
    "IBP", "ICFI", "IDEX", "IEX", "IIIV", "IIIN", "INDB", "INFN",
    "INGR", "INVA", "IONS", "IRT", "ITT", "ITUOY",
    # J
    "JACK", "JBGS", "JHG", "JLL", "JNPR", "JOBY", "JSPR",
    # K
    "KBH", "KMPR", "KNF", "KNX", "KRC", "KRG", "KTOS",
    # L
    "LAD", "LANC", "LBRT", "LHX", "LIVN", "LKQ", "LNTH", "LPX",
    "LSTR", "LUMN",
    # M
    "MAT", "MBIN", "MC", "MGEE", "MGY", "MHO", "MKSI", "MMSI",
    "MMS", "MNRO", "MOG.A", "MRCY", "MRC", "MTH", "MTN", "MTUS",
    "MTX", "MUR",
    # N
    "NATL", "NBT", "NBTB", "NEP", "NFG", "NGVT", "NJR", "NLY",
    "NNN", "NOG", "NRC", "NSIT", "NSP", "NTCT", "NUS", "NWBI",
    # O
    "OFG", "OGS", "OI", "OKE", "OLLI", "OMCL", "OMF", "ORA",
    "ORAN", "OUT",
    # P
    "PCRX", "PDM", "PENN", "PFSI", "PII", "PINC", "PLXS", "PNFP",
    "PNTG", "POST", "PPBI", "PRG", "PRGS", "PRGS", "PRK", "PSA",
    "PSN", "PTC",
    # Q
    "QCRH", "QLYS",
    # R
    "RBC", "RBCAA", "RCM", "RDNT", "RES", "RGLD", "RHP", "RLI",
    "RMBS", "RNR", "ROG", "ROIC", "RPM", "RPAI", "RUSHA",
    # S
    "SABR", "SAFE", "SAIA", "SANM", "SBOW", "SBSI", "SCSC", "SFM",
    "SHO", "SIG", "SJW", "SKT", "SLG", "SM", "SMAR", "SMG", "SNV",
    "SONO", "SPN", "SPSC", "STC", "STRA", "STRL", "SUM", "SWX",
    # T
    "TALO", "TGNA", "THG", "TISI", "TMHC", "TNL", "TNET", "TOWN",
    "TPH", "TRMK", "TRN", "TRMK", "TXRH",
    # U
    "UBSI", "UE", "UFI", "UGI", "UMBF", "UNFI", "UNIT", "UNM",
    "USCF", "USPH",
    # V
    "VBTX", "VCNX", "VECO", "VFC", "VIRT", "VLY", "VMEO", "VNTR",
    "VSAT", "VSH",
    # W
    "WABC", "WAFD", "WBS", "WDFC", "WEN", "WKC", "WLY", "WLYB",
    "WMS", "WOR", "WS", "WTBA", "WTFC", "WTS",
    # X / Y / Z
    "XHR", "XPEL",
    "YOU",
    "ZWS",
]

# Lookupsets for fast tests
SP400_SET:    frozenset[str] = frozenset(SP400)
WATCHLIST_SET: frozenset[str] = frozenset(WATCHLIST)

SECTOR_MAP: dict[str, list[str]] = {
    "Technology":   ["NVDA", "AMD", "AKAM", "COHU", "FORM", "INFN", "MKSI", "PLXS", "RMBS", "SMCI"],
    "Financials":   ["AFG", "ARI", "ASB", "BOH", "CBSH", "CFR", "FHN", "HLI", "HWC", "KMPR"],
    "Energy":       ["APA", "CHRD", "CRL", "DEN", "MGY", "MUR", "NOG", "SM", "TALO"],
    "Industrials":  ["ACM", "AGCO", "AIT", "ALLE", "AWI", "CR", "GATX", "GVA", "ITT", "KNX"],
    "Healthcare":   ["ACHC", "AMN", "GKOS", "GMED", "HAE", "HALO", "IONS", "MMSI", "OMCL"],
    "Consumer":     ["AEO", "BOOT", "DKS", "DPZ", "EAT", "HOG", "LKQ", "MAT", "OLLI", "SFM"],
    "REITs":        ["BNL", "BXMT", "COPT", "EGP", "EPR", "FR", "JBGS", "NNN", "ROIC", "SLG"],
    "Utilities":    ["AVA", "BKH", "CWT", "MGE", "NJR", "OGS", "SJW", "SWX", "UGI"],
    "Materials":    ["ALB", "ATI", "AVN", "CBT", "CLF", "GEF", "GPK", "LPX", "RPM", "SMG"],
}