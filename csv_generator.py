import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

# Lista symboli giełdowych - można dodać więcej firm
tickers = [
    "AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META", "NVDA", "BABA", "NFLX", "INTC", "AMD", "CSCO", "ORCL", "IBM",
    "QCOM", "AVGO", "TXN", "ADBE", "CRM", "INTU", "AMAT", "MU", "LRCX", "KLAC", "AMD", "NVDA", "AMZN", "TSLA",
    "MSFT", "AAPL", "GOOG", "GOOGL", "META", "NFLX", "TSM", "ASML", "BIDU", "JD", "NTES", "PDD", "BABA", "TCEHY",
    "UBER", "LYFT", "SNAP", "TWTR", "PINS", "ZM", "SQ", "PYPL", "SHOP", "DOCU", "SPOT", "SE", "BILI", "MELI", "ETSY",
    "RBLX", "PLTR", "TWLO", "DDOG", "FSLY", "NET", "CRWD", "SPLK", "ZS", "OKTA", "MDB", "SNOW", "PD", "U", "WORK",
    "WIX", "FVRR", "UPWK", "ZI", "PATH", "AI", "PLUG", "FCEL", "BLDP", "SPCE", "SPCE", "MAXR", "NIO", "LI", "XPEV",
    "RIVN", "LCID", "QS", "NKLA", "WKHS", "BLNK", "CHPT", "RIOT", "MARA", "HUT", "BTBT", "V", "MA", "AXP", "DFS",
    "COF", "SYF", "ALLY", "C", "JPM", "BAC", "WFC", "GS", "MS", "USB", "PNC", "TFC", "SCHW", "AMTD", "ETRADE", "IBKR",
    "FISV", "FIS", "GPN", "PYPL", "SQ", "NDAQ", "ICE", "CME", "MKTX", "MSCI", "SPGI", "MCO", "DOW", "DD", "EMN",
    "LYB", "PPG", "SHW", "APD", "LIN", "ECL", "NUE", "STLD", "X", "CLF", "AA", "BA", "GE", "HON", "MMM", "CAT", "DE",
    "PCAR", "CMI", "EMR", "ROK", "ETN", "PH", "DOV", "XYL", "ITW", "SWK", "IR", "FTV", "GWW", "URI", "TEX", "MTD",
    "PKI", "WAT", "A", "DHR", "TMO", "IQV", "BIO", "TECH", "ZBH", "SYK", "BSX", "MDT", "ISRG", "EW", "RMD", "GMED",
    "IART", "PEN", "NUVA", "XRAY", "ALGN", "STE", "A", "RGEN", "BIO", "AVTR", "WAT", "MTD", "TMO", "DHR", "PKI", "IQV",
    "MNST", "PEP", "KO", "COST", "WMT", "TGT", "KR", "DG", "DLTR", "BJ", "COST", "WMT", "TGT", "KR", "DG", "DLTR",
    "BJ", "CVS", "WBA", "RAD", "AMZN", "EBAY", "W", "OSTK", "FTCH", "ETSY", "MELI", "BABA", "JD", "PDD", "BIDU",
    "SHOP", "SE", "RBLX", "PLTR", "U", "SNOW", "DDOG", "ZM", "TWLO", "DOCU", "OKTA", "CRWD", "SPLK", "ZS", "NET",
    "FSLY", "PD", "MDB", "WKHS", "FUBO", "PINS", "SNAP", "TWTR", "LYFT", "UBER", "AAL", "DAL", "UAL", "LUV", "ALK",
    "JBLU", "SAVE", "RYAAY", "WIZZ", "LHA", "ICAGY", "EADSY", "BA", "AIR", "NOC", "LMT", "GD", "HII", "TXT", "LDOS",
    "SAIC", "BWXT", "OSK", "AXON", "EV", "BA", "HON", "MMM", "CAT", "DE", "PCAR", "CMI", "EMR", "ROK", "ETN", "PH",
    "DOV", "XYL", "ITW", "SWK", "IR", "FTV", "GWW", "URI", "TEX", "ABB", "EMR", "ROK", "HON", "GE", "MMM", "ITW", "ETN",
    "PH", "SWK", "IR", "XYL", "DOV", "URI", "TEX", "AL", "CCL", "RCL", "NCLH", "LVS", "WYNN", "MGM", "MLCO", "PENN",
    "DKNG", "RRR", "BYD", "CHDN", "CZR", "BALY", "MCRI", "GDEN", "LVS", "WYNN", "MGM", "MLCO", "PENN", "DKNG", "RRR",
    "BYD", "CHDN", "CZR", "BALY", "MCRI", "GDEN", "MTCH", "IAC", "BMBL", "FB", "TWTR", "SNAP", "PINS", "SPOT", "SQ",
    "PYPL", "AFRM", "UPST", "SOFI", "ROKU", "NFLX", "DIS", "CMCSA", "FOX", "VIAC", "VIAC", "DISCA", "AMCX", "GTN",
    "NXST", "SCS", "HMHC", "EDU", "TAL", "GSX", "DAO", "TME", "ATHM", "BILI", "BIDU", "NTES", "PDD", "JD", "BABA",
    "IQ", "WB", "YY", "HUYA", "DOYU", "LIZI", "GOTU", "TIGR", "FUTU", "TME", "ATHM", "BILI", "BIDU", "NTES", "PDD",
    "JD", "BABA", "IQ", "WB", "YY", "HUYA", "DOYU", "LIZI", "GOTU", "TIGR", "FUTU", "ADBE", "CRM", "INTU", "ADSK",
    "MSFT", "ORCL", "SAP", "NOW", "WDAY", "ZEN", "CRM", "DOCU", "ADBE", "SPLK", "SNOW", "MDB", "DDOG", "ZS", "OKTA",
    "CRWD", "PANW", "FTNT", "FEYE", "CHKP", "JNPR", "CSCO", "ANET", "PALO", "NET", "AKAM", "FSLY", "ZM", "TWLO",
    "SPOT", "U", "SNOW", "MDB", "DDOG", "ZS", "OKTA", "CRWD", "PANW", "FTNT", "FEYE", "CHKP", "JNPR", "CSCO", "ANET",
    "PALO", "NET", "AKAM", "FSLY", "WMT", "COST", "TGT", "BBY", "HD", "LOW", "TSCO", "ORLY", "AAP", "AZO", "GPC",
    "GM", "F", "TSLA", "HMC", "TM", "NSANY", "VWAGY", "DDAIF", "STLA", "BMWYY", "FCAU", "RACE", "GM", "F", "TSLA",
    "HMC", "TM", "NSANY", "VWAGY", "DDAIF", "STLA", "BMWYY", "FCAU", "RACE"
]

# Zakres dat
start_date = "2020-01-01"
end_date = "2024-08-01"

# Tworzenie folderu na dane, jeśli jeszcze nie istnieje
if not os.path.exists('dane_akcje'):
    os.makedirs('dane_akcje')

# Pobieranie danych dla każdej firmy
for ticker in tickers:
    df = yf.download(ticker, start=start_date, end=end_date)
    file_name = f'dane_akcje/{ticker}.csv'
    df.to_csv(file_name)
    print(f"Pobrano dane dla {ticker} i zapisano do {file_name}")
