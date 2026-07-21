import json
import os

import pandas as pd
from utils import RAW_DATA_PATH, CONFIG_PATH, PROCESSED_DATA_PATH, read_config


config = read_config(CONFIG_PATH)


def read_file(file_path: str) -> dict:
    """
    Baca file json mentah dari folder raw_data
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data_json = json.load(f)
        print(f"Sukses membaca file dari: {file_path}")
        return data_json
    
    except FileNotFoundError:
        print(f"Error: File tidak ditemukan di {file_path}")
        return False
    except json.JSONDecodeError:
        print(f"Error: Format file JSON rusak atau tidak valid")
        return False
    except Exception as e:
        print(f"Terjadi error tak terduga: {e}")
        return False


def transform(data: list | dict) -> pd.DataFrame:
    """
    Melakukan transformasi terhadap data mentah
    """
    df = pd.DataFrame(data)
    if (df['rate'] <= 0).any():
        print("Peringatan: ditemukan rate <= 0 di data")
    if df['rate'].isnull().any():
        print("Peringatan: ditemukan nilai rate yang kosong (null)")
    df["base"] = df["base"].astype("category")
    df["quote"] = df["quote"].astype("category")
    df["date"] = pd.to_datetime(df["date"])
    df['inverse_rate'] = (1 / df['rate']).round(2)
    return df


def save_to_csv(df: pd.DataFrame, file_path: str) -> bool:
    """
    Simpan dataframe ke bentuk csv
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)
        print(f"Data berhasil disimpan ke: {file_path}")
        return True
    
    except Exception as e:
        print(f"Gagal menyimpan ke CSV: {e}")
        return False


def run_transform(processed_data_path: str):
    """
    Baca file raw json, lakukan transformasi dan simpan ke csv
    """
    raw_file_name = f"rates_{config['date']['from']}_to_{config['date']['to']}.json"
    raw_file_path = os.path.join(RAW_DATA_PATH, raw_file_name)
    df_file_name = f"rates_{config['date']['from']}_to_{config['date']['to']}.csv"
    df_file_path = os.path.join(PROCESSED_DATA_PATH, df_file_name)
    data = read_file(raw_file_path)
    
    try:
        if data:
            df = transform(data)
            is_saved = save_to_csv(df, df_file_path)
            return is_saved
        else:
            print("Gagal membaca file")
            return False
    except Exception as e:
        print("Gagal melakukan transformasi pada data")
        return False
    

if __name__ == "__main__":
    run_transform(PROCESSED_DATA_PATH)