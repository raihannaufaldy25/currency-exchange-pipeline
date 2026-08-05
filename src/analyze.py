import os
import pandas as pd

from sqlalchemy.engine import Engine
from utils import SQL_PATH, get_db_engine


def read_sql_file(file_path: str) -> str:
    """
    Baca file sql script dari folder sql
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_sql = file.read()
        print(f"Sukses membaca file dari: {file_path}")
        return file_sql
    except FileNotFoundError:
        print(f"Error: File tidak ditemukan di {file_path}")
        return False
    except Exception as e:
        print(f"Terjadi error tak terduga: {e}")
        return False


def read_query(query: str, engine: Engine) -> pd.DataFrame | bool:
    """
    Eksekusi query sql lalu return sebagai dataframe
    """
    try:
        df = pd.read_sql(query, engine)
        print("Berhasil membaca query")
        return df

    except Exception as e:
        print(f"Terjadi error: {e}")
        return False


def run_analyze(sql_file_path: str) -> bool:
    """
    Baca file sql lalu eksekusi querynya
    """
    file_sql = read_sql_file(sql_file_path)
    engine = get_db_engine()

    try:
        if file_sql and engine:
            analysis = read_query(file_sql, engine)
            print(analysis)
            return True
        else:
            print("Gagal mengeksekusi query")
            return False

    except Exception as e:
        print(f"Terjadi error: {e}")
        return False


if __name__ == "__main__":
    pct_rate_change = os.path.join(SQL_PATH, "pct_rate_change.sql")
    weekly_rate_avg = os.path.join(SQL_PATH, "weekly_avg.sql")
    volatility_rate = os.path.join(SQL_PATH, "volatility_rate.sql")
    overall_performance = os.path.join(SQL_PATH, "overall_performance.sql")
    run_analyze(overall_performance)