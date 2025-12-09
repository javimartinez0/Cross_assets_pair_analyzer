import yfinance as yf
import pandas as pd
from pathlib import Path  

# Funcion reutilizable para descargar y guardar datos de yfinance

def download_data(tickers, start, end, interval="1d", save_path="data/raw/prices.csv"):
    df = yf.download(tickers, start=start, end=end, interval=interval, auto_adjust=True)
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    df.to_csv(save_path)
    return df

# Funcion para cargar y preparar los precios de cierre 
def load_and_prepare_closes(path="data/raw/prices.csv", preferred_fields=("Close", "Adj Close", "Price")):
    try:
        df = pd.read_csv(path, header=[0, 1], index_col=0, parse_dates=True)
        multi = isinstance(df.columns, pd.MultiIndex)
    except ValueError:
        df = pd.read_csv(path, header=0, index_col=0, parse_dates=True)
        multi = False

    if multi:
        top = df.columns.get_level_values(0)
        field = next((f for f in preferred_fields if f in top), None)
        if field is None:
            raise KeyError(f"No se encontraron {preferred_fields}. Disponibles: {top.unique().tolist()}")
        closes = df[field].copy()
        closes.columns.name = None
    else:
        field = next((f for f in preferred_fields if any(col.startswith(f) for col in df.columns)), None)
        if field is None:
            raise KeyError(f"No se encontraron {preferred_fields}. Disponibles: {list(df.columns)}")
        closes = df[[c for c in df.columns if c.startswith(field)]].copy()
        closes.columns = [c.replace(f"{field}.", "") for c in closes.columns]

    closes = closes.dropna(how="all").ffill().dropna()
    return closes

