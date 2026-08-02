import os

import yaml
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


load_dotenv()

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.abspath(os.path.join(CURRENT_PATH, "..", "config.yaml"))
RAW_DATA_PATH = os.path.abspath(os.path.join(CURRENT_PATH, "..", "raw_data"))
PROCESSED_DATA_PATH = os.path.abspath(os.path.join(CURRENT_PATH, "..", "processed_data"))
SQL_PATH = os.path.abspath(os.path.join(CURRENT_PATH, "..", "sql"))


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


def get_db_engine() -> Engine | bool:
    """
    Membuat koneksi (engine) ke database PostgreSQL menggunakan
    kredensial dari environment variable (.env)
    """
    try:
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")

        connection_string = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        engine = create_engine(connection_string)
        print("Berhasil membuat koneksi ke database")
        return engine

    except Exception as e:
        print(f"Gagal membuat koneksi ke database: {e}")
        return False