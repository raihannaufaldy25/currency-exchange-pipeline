import json
import os

import requests
import yaml


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.abspath(os.path.join(CURRENT_PATH, "..", "config.yaml"))
RAW_DATA_PATH = os.path.abspath(os.path.join(CURRENT_PATH, "..", "raw_data"))
BASE_URL = "https://api.frankfurter.dev/v2/rates"

def read_config(config_path: str) -> dict:
    """
    Baca file config YAML dan return sebagai dictionary
    """
    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        
        print("Berhasil membaca config")
        return config
    
    except FileNotFoundError:
        print(f"Error: File tidak ditemukan di {config_path}")
        raise
    except yaml.YAMLError as exc:
        print(f"Error saat membaca file YAML: {exc}")
        raise


def extract_from_api(base_url: str, base_currency: str, quote_currency: str, date_from: str, date_to: str) -> dict | list | bool:
    """
    Mengambil data dari API
    """
    params = {
        "from": date_from,
        "to": date_to,
        "base": base_currency,
        "quotes": quote_currency
    }

    try:
        response = requests.get(base_url, params)
        response.raise_for_status()
        data = response.json()
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error terjadi: {http_err}")
        return False
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Gagal terhubung ke server: {conn_err}")
        return False
    except requests.exceptions.Timeout:
        print("Waktu permintaan habis (Timeout)")
        return False
    except requests.exceptions.RequestException as err:
        print(f"Terjadi error tak terduga: {err}")
        return False


def save_to_json(data: dict, file_path: str):
    """
    Menyimpan data mentah hasil ekstrasi ke dalam json
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data berhasil disimpan ke: {file_path}")
        return True
    
    except Exception as e:
        print(f"Gagal menyimpan ke JSON: {e}")
        return False


def run_pipeline(base_url: str, config_path: str, raw_data_path: str) -> bool:
    """
    Membaca config, extract data, lalu simpan file
    """
    config = read_config(config_path)
    base_currency = config['currency']['base']
    quote_currency = ','.join(config['currency']['quote'])
    date_from = config['date']['from']
    date_to = config['date']['to']

    data = extract_from_api(base_url, base_currency, quote_currency, date_from, date_to)

    file_name = f"rates_{date_from}_to_{date_to}.json"
    file_path = os.path.join(raw_data_path, file_name)

    if data:
        is_saved = save_to_json(data, file_path)
        return is_saved
    else:
        print("Gagal mengekstrak data")
        return False

if __name__ == "__main__":
    run_pipeline(BASE_URL, CONFIG_PATH, RAW_DATA_PATH)