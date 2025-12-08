import yfinance as yf
import pandas as pd
from pathlib import Path  

# Funcion reutilizable para descargar y guardar datos de yfinance

def download_data(tickers, start, end, interval="1d", save_path="data/raw/prices.csv"):
    df = yf.download(tickers, start=start, end=end, interval=interval, auto_adjust=True)
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    df.to_csv(save_path)
    return df

