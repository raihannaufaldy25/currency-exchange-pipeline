import os

import pandas as pd
from sqlalchemy.engine import Engine

from utils import PROCESSED_DATA_PATH, CONFIG_PATH, read_config, get_db_engine


config = read_config(CONFIG_PATH)

TABLE_NAME = "exchange_rates"


def read_csv_file(file_path: str) -> pd.DataFrame | bool:
    """
    Baca file CSV hasil transform, kembalikan sebagai DataFrame
    """
    try:
        df = pd.read_csv(file_path, parse_dates=["date"])
        print(f"Sukses membaca file dari: {file_path}")
        return df
    
    except FileNotFoundError:
        print(f"Error: File tidak ditemukan di {file_path}")
        return False
    except Exception as e:
        print(f"Terjadi error tak terduga: {e}")
        return False


def load_to_db(df: pd.DataFrame, table_name: str, engine: Engine) -> bool:
    """
    Load DataFrame ke tabel PostgreSQL.
    if_exists="replace" dipakai supaya setiap run pipeline ini
    menghasilkan data yang konsisten (tidak menumpuk duplikat
    kalau script dijalankan berkali-kali dengan data yang sama).
    """
    try:
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        print(f"Berhasil load {len(df)} baris ke tabel '{table_name}'")
        return True

    except Exception as e:
        print(f"Gagal load data ke database: {e}")
        return False


def run_load(processed_data_path: str, table_name: str) -> bool:
    """
    Baca file CSV hasil transform, lalu load ke PostgreSQL
    """
    csv_file_name = f"rates_{config['date']['from']}_to_{config['date']['to']}.csv"
    csv_file_path = os.path.join(processed_data_path, csv_file_name)

    df = read_csv_file(csv_file_path)
    if df is False:
        print("Gagal membaca file CSV, proses load dihentikan")
        return False

    engine = get_db_engine()
    if engine is False:
        print("Gagal terhubung ke database, proses load dihentikan")
        return False

    return load_to_db(df, table_name, engine)


if __name__ == "__main__":
    run_load(PROCESSED_DATA_PATH, TABLE_NAME)